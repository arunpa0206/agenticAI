import random
import difflib
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool


# ============================================================
# LLM
# ============================================================

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key="",
    temperature=0
)

current_flight = None


# ============================================================
# Flight Database
# ============================================================

flights = [

{
"flight_id":"FL101",
"airline":"IndiGo",
"from":"Bangalore",
"to":"Delhi",
"time":"6:30 PM",
"price":5200
},

{
"flight_id":"FL202",
"airline":"Air India",
"from":"Bangalore",
"to":"Delhi",
"time":"8:15 PM",
"price":6100
},

{
"flight_id":"FL303",
"airline":"Vistara",
"from":"Bangalore",
"to":"Delhi",
"time":"9:45 PM",
"price":5700
}

]


# ============================================================
# Normalize
# ============================================================

city_map = {

"bengaluru":"bangalore",
"blr":"bangalore",
"del":"delhi"

}


def normalize(city):

    city = city.lower()

    if city in city_map:
        return city_map[city]

    matches = difflib.get_close_matches(
        city,
        ["bangalore","delhi"],
        n=1,
        cutoff=0.7
    )

    return matches[0] if matches else city


# ============================================================
# Tools
# ============================================================

@tool
def search_flights(source:str, destination:str):
    """Search flights"""

    source = normalize(source)
    destination = normalize(destination)

    matches = []

    for flight in flights:

        if (
            flight["from"].lower() == source
            and
            flight["to"].lower() == destination
        ):
            matches.append(flight)

    if not matches:
        return {"message":"No flights"}

    return random.choice(matches)


@tool
def book_flight(flight_id:str):
    """Book flight"""

    return {

        "booking_id":
        f"BK{random.randint(1000,9999)}",

        "flight_id":
        flight_id

    }


@tool
def cancel_flight(flight_id:str):
    """Cancel flight"""

    return {

        "flight_id":
        flight_id

    }
# ============================================================
# State
# ============================================================

class AgentState(TypedDict):

    user_input: str
    plan: object
    response: str


# ============================================================
# Node 1
# Generate Plan
# ============================================================

llm_tools = llm.bind_tools(
    [
        search_flights,
        book_flight,
        cancel_flight
    ]
)


def generate_plan(state):

    global current_flight

    prompt = state["user_input"]

    # Give Claude the current flight context if one exists
    if current_flight:

        prompt = f"""
You are an AI Flight Assistant.

Current selected flight:

Flight ID : {current_flight['flight_id']}
Airline   : {current_flight['airline']}
From      : {current_flight['from']}
To        : {current_flight['to']}
Time      : {current_flight['time']}
Price     : ₹{current_flight['price']}

User request:
{state["user_input"]}

Instructions:

- If the user says "book this flight", "book it",
  or anything similar, call book_flight()
  using the current flight_id.

- If the user says "cancel this flight",
  "cancel it", or anything similar,
  call cancel_flight() using the current flight_id.

- If the user says "generate another flight",
  "another flight", "show another flight",
  or anything similar,
  call search_flights() using the SAME
  source and destination as the current flight.

- Otherwise, interpret the request normally
  and choose the correct tool.
"""

    plan = llm_tools.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )

    return {
        "plan": plan
    }
# ============================================================
# Node 2
# Execute Plan
# ============================================================

def execute_plan(state):

    global current_flight

    plan = state["plan"]

    if not plan.tool_calls:

        return {
            "response": plan.content
        }

    tool_call = plan.tool_calls[0]

    name = tool_call["name"]

    args = tool_call["args"]


    # ========================================================
    # Search Flights
    # ========================================================

    if name == "search_flights":

        result = search_flights.invoke(args)

        if "message" in result:

            return {
                "response": result["message"]
            }

        current_flight = result

        return {

            "response": f"""

==================================================
Recommended Flight
==================================================

Flight ID : {result['flight_id']}
Airline   : {result['airline']}
Route     : {result['from']} → {result['to']}
Time      : {result['time']}
Price     : ₹{result['price']}

You can now say:

• Book this flight
• Generate another flight
• Cancel this flight

"""
        }


    # ========================================================
    # Book Flight
    # ========================================================

    elif name == "book_flight":

        result = book_flight.invoke(args)

        return {

            "response": f"""

==================================================
Flight Confirmed
==================================================

Booking ID : {result['booking_id']}
Flight ID  : {result['flight_id']}

"""
        }


    # ========================================================
    # Cancel Flight
    # ========================================================

    elif name == "cancel_flight":

        result = cancel_flight.invoke(args)

        return {

            "response": f"""

==================================================
Flight Cancelled
==================================================

Flight ID : {result['flight_id']}

"""
        }


    return {
        "response": "I couldn't understand the request."
    }


# ============================================================
# Graph
# ============================================================

graph = StateGraph(
    AgentState
)

graph.add_node(
    "generate_plan",
    generate_plan
)

graph.add_node(
    "execute_plan",
    execute_plan
)

graph.set_entry_point(
    "generate_plan"
)

graph.add_edge(
    "generate_plan",
    "execute_plan"
)

graph.add_edge(
    "execute_plan",
    END
)

app = graph.compile()