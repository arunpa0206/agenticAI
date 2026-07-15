import os
from typing import TypedDict, Literal
from dotenv import load_dotenv

# Import LangGraph and LangChain components
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

# Load environment variables (e.g. ANTHROPIC_API_KEY)
load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY not found.")

# Instantiate the Anthropic LLM model
llm = ChatAnthropic(
    model="claude-sonnet-5",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


# =====================================================================
# Tools Definition
# =====================================================================

@tool
def search_flights(source: str, destination: str):
    """
    Search flights from a source city to a destination city.
    """
    return {
        "legs": [
            {
                "flight_id": "FL101",
                "from": source.title(),
                "to": "Mumbai",
                "time": "10:00 AM",
                "price": 4500,
            },
            {
                "flight_id": "FL102",
                "from": "Mumbai",
                "to": destination.title(),
                "time": "4:30 PM",
                "price": 5200,
            },
        ]
    }


@tool
def book_flight(flight_ids: list):
    """
    Book flights using a list of flight IDs.
    """
    return {
        "bookings": [
            {
                "booking_id": f"BK{1000+i}",
                "flight_id": fid
            }
            for i, fid in enumerate(flight_ids)
        ]
    }


@tool
def cancel_flight(flight_ids: list):
    """
    Cancel booked flights by providing their flight IDs.
    """
    return {"cancelled": flight_ids}


# =====================================================================
# State and Bindings
# =====================================================================

# Define the shared state schema for our LangGraph agent
class FlightState(TypedDict):
    user_input: str                                     # User's raw text query
    intent: Literal["search", "book", "cancel", "end"]  # Classified user intent
    flights: list                                       # Current active flight search results
    bookings: list                                      # Active bookings
    response: str                                       # Final message returned to the user

# Bind the flight tools to the LLM model
llm_tools = llm.bind_tools(
    [search_flights, book_flight, cancel_flight]
)


# =====================================================================
# Graph Nodes and Step Logic
# =====================================================================

def input_guardrail_node(state: FlightState):
    """
    Node 1: Evaluates the user input using the Input Guardrail model.
    Checks for malicious queries, prompt injections, or irrelevant queries.
    """
    from inputguardrail import input_guardrail
    is_safe, message = input_guardrail(llm, state["user_input"])
    
    # If the guardrail blocks the input, we save the reason in state["response"]
    if not is_safe:
        return {"response": message}
    return {"response": ""}


def route_guardrail(state: FlightState):
    """
    Conditional Edge Router: Decides whether to proceed or terminate based on 
    the input guardrail result.
    """
    if state.get("response", "").startswith("BLOCK:"):
        return "blocked"  # Route to END
    return "allowed"      # Route to the intent classifier (router)


def output_guardrail_node(state: FlightState):
    """
    Node 7 (Output Guardrail): Runs safety check on the final response content.
    """
    from outputguardrail import output_guardrail
    is_safe, message = output_guardrail(llm, state["response"])
    if not is_safe:
        return {"response": message}
    return {}


def router(state: FlightState):
    """
    Node 2: Intent Classifier.
    Analyzes the user's input and classifies the intent into search, book, or cancel.
    """
    prompt = f"""
You are an intent classifier.

User:
{state["user_input"]}

Return ONE tool:
- search_flights
- book_flight
- cancel_flight
"""
    # Ask LLM to determine the appropriate tool call
    msg = llm_tools.invoke([HumanMessage(content=prompt)])

    if msg.tool_calls:
        tool_name = msg.tool_calls[0]["name"]
    else:
        # Fallback to simple keyword parsing if tool binding is empty
        text = state["user_input"].lower()
        if "cancel" in text:
            tool_name = "cancel_flight"
        elif "book" in text:
            tool_name = "book_flight"
        else:
            tool_name = "search_flights"

    # Evaluate the tool access guardrail
    from toolguardrail import tool_guardrail
    is_allowed, reason = tool_guardrail(llm, state["user_input"], tool_name)
    if not is_allowed:
        return {"intent": "end", "response": reason}

    if tool_name == "search_flights":
        return {"intent": "search"}

    if tool_name == "book_flight":
        return {"intent": "book"}

    return {"intent": "cancel"}


def route(state):
    """
    Conditional Edge Router: Routes the execution flow from the intent classifier
    to the respective task handler node.
    """
    return state["intent"]


def generate_flight(state: FlightState):
    """
    Node 3 (Search): Extracts source/destination cities and calls the search tool.
    """
    text = state["user_input"].lower()
    words = text.replace("?", "").split()

    source = ""
    destination = ""

    # Basic entity extraction for cities from query
    if "from" in words and "to" in words:
        source = words[words.index("from")+1]
        destination = words[words.index("to")+1]
    elif "to" in words:
        to_idx = words.index("to")
        if to_idx > 0:
            source = words[to_idx - 1]
        else:
            source = "Bangalore"
        destination = words[to_idx + 1]
    else:
        source = "Bangalore"
        destination = "Delhi"

    # Search flights using the tool
    result = search_flights.invoke(
        {
            "source": source,
            "destination": destination,
        }
    )

    # Format the response message
    return {
        "flights": result["legs"],
        "user_input": state["user_input"],
        "response":
            "\n".join(
                f'{f["flight_id"]}: {f["from"]} -> {f["to"]} ₹{f["price"]}'
                for f in result["legs"]
            )
    }


def book_flight_node(state: FlightState):
    """
    Node 4 (Book): Books the flights currently stored in the active flights state.
    """
    ids = [f["flight_id"] for f in state["flights"]]

    result = book_flight.invoke(
        {
            "flight_ids": ids
        }
    )

    return {
        "bookings": result["bookings"],
        "response":
            "Booked:\n"
            + "\n".join(
                f'{b["booking_id"]} ({b["flight_id"]})'
                for b in result["bookings"]
            )
    }


def cancel_flight_node(state: FlightState):
    """
    Node 5 (Cancel): Cancels active bookings.
    """
    ids = [b["flight_id"] for b in state["bookings"]]

    cancel_flight.invoke(
        {
            "flight_ids": ids
        }
    )

    return {
        "bookings": [],
        "flights": [],
        "response": "Flights cancelled."
    }


def ask_cancel_choice(state: FlightState):
    """
    Node 6: Handles post-cancellation dialog, prompting user to search again or exit.
    """
    print("\nAgent:")
    print("Flights cancelled.")
    
    choice = input("Do you want to generate another plan or end? ").strip().lower()
    
    if "generate" in choice or "another" in choice or "plan" in choice or "yes" in choice or choice == "y":
        route_input = input("From where to where would you like to go? ")
        return {
            "intent": "search",
            "user_input": route_input,
            "response": ""
        }
    return {
        "intent": "end",
        "response": "Session ended."
    }


def after_cancel(state):
    """
    Conditional Edge Router: Decides where to route after a cancellation choice is made.
    """
    if state["intent"] == "search":
        return "generate"
    return "end"


# =====================================================================
# Graph Construction and Compilation
# =====================================================================

graph = StateGraph(FlightState)

# Register nodes to the graph
graph.add_node("input_guardrail", input_guardrail_node)
graph.add_node("router", router)
graph.add_node("generate_flight", generate_flight)
graph.add_node("book_flight", book_flight_node)
graph.add_node("cancel_flight", cancel_flight_node)
graph.add_node("ask_cancel_choice", ask_cancel_choice)
graph.add_node("output_guardrail", output_guardrail_node)

# Define entry point (flows first to the input guardrail)
graph.set_entry_point("input_guardrail")

# Define conditional transition from Input Guardrail
graph.add_conditional_edges(
    "input_guardrail",
    route_guardrail,
    {
        "blocked": END,       # Direct termination on validation block
        "allowed": "router",  # Transition to classification node if safe
    },
)

# Define conditional transitions from Intent Classifier
graph.add_conditional_edges(
    "router",
    route,
    {
        "search": "generate_flight",
        "book": "book_flight",
        "cancel": "cancel_flight",
        "end": END,
    },
)

# Define transitions from task handlers (flowing to the output guardrail)
graph.add_edge("generate_flight", "output_guardrail")
graph.add_edge("book_flight", "output_guardrail")
graph.add_edge("cancel_flight", "ask_cancel_choice")

# Define conditional transitions from post-cancellation choices (flowing to output guardrail when ending)
graph.add_conditional_edges(
    "ask_cancel_choice",
    after_cancel,
    {
        "generate": "generate_flight",
        "end": "output_guardrail",
    },
)

# Define the final transition from Output Guardrail to END
graph.add_edge("output_guardrail", END)

# Compile graph into a runnable application
app = graph.compile()
