import os
from typing import TypedDict, Literal
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

load_dotenv(override=True)

if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY not found.")

llm = ChatAnthropic(
    model="claude-sonnet-5",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# -----------------------------
# Tools
# -----------------------------
@tool
def search_flights(source: str, destination: str):
    """Search flights."""
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
    """Book flights."""
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
    """Cancel booked flights."""
    return {"cancelled": flight_ids}


class FlightState(TypedDict):
    user_input: str
    intent: Literal["search", "book", "cancel", "end"]
    flights: list
    bookings: list
    response: str


llm_tools = llm.bind_tools(
    [search_flights, book_flight, cancel_flight]
)


def router(state: FlightState):
    prompt = f"""
You are an intent classifier.

User:
{state["user_input"]}

Return ONE tool:
- search_flights
- book_flight
- cancel_flight
"""
    msg = llm_tools.invoke([HumanMessage(content=prompt)])

    if msg.tool_calls:
        tool = msg.tool_calls[0]["name"]

        if tool == "search_flights":
            return {"intent": "search"}

        if tool == "book_flight":
            return {"intent": "book"}

        return {"intent": "cancel"}

    text = state["user_input"].lower()

    if "cancel" in text:
        return {"intent": "cancel"}

    if "book" in text:
        return {"intent": "book"}

    return {"intent": "search"}


def generate_flight(state: FlightState):
    text = state["user_input"].lower()

    words = text.replace("?", "").split()

    source = ""
    destination = ""

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

    result = search_flights.invoke(
        {
            "source": source,
            "destination": destination,
        }
    )

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


def route(state):
    return state["intent"]


def after_cancel(state):
    if state["intent"] == "search":
        return "generate"
    return "end"


graph = StateGraph(FlightState)

graph.add_node("router", router)
graph.add_node("generate_flight", generate_flight)
graph.add_node("book_flight", book_flight_node)
graph.add_node("cancel_flight", cancel_flight_node)
graph.add_node("ask_cancel_choice", ask_cancel_choice)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    route,
    {
        "search": "generate_flight",
        "book": "book_flight",
        "cancel": "cancel_flight",
    },
)

graph.add_edge("generate_flight", END)
graph.add_edge("book_flight", END)
graph.add_edge("cancel_flight", "ask_cancel_choice")

graph.add_conditional_edges(
    "ask_cancel_choice",
    after_cancel,
    {
        "generate": "generate_flight",
        "end": END,
    },
)

app = graph.compile()
