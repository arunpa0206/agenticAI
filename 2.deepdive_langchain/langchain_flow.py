import random
import difflib
from typing import TypedDict

from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool


# ============================================================
# LLM
# ============================================================

llm = ChatAnthropic(
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-5",
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
# City Normalize
# ============================================================

city_map = {
    "bengaluru":"bangalore",
    "blr":"bangalore",
    "del":"delhi"
}


def normalize(city):

    city = city.lower().strip()

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
def search_flights(source:str,destination:str):
    """Search flights between source and destination."""

    source = normalize(source)
    destination = normalize(destination)

    results=[]

    for flight in flights:

        if(
            flight["from"].lower()==source
            and
            flight["to"].lower()==destination
        ):
            results.append(flight)

    if not results:
        return {"message":"No flights found"}

    return random.choice(results)


@tool
def book_flight(flight_id:str):
    """Book a flight using flight id."""

    return {
        "booking_id":f"BK{random.randint(1000,9999)}",
        "flight_id":flight_id
    }


@tool
def cancel_flight(flight_id:str):
    """Cancel booked flight using flight id."""

    return {
        "flight_id":flight_id
    }


# ============================================================
# Bind tools
# ============================================================

llm_tools = llm.bind_tools(
    [
        search_flights,
        book_flight,
        cancel_flight
    ]
)


# ============================================================
# State
# ============================================================

class AgentState(TypedDict):

    user_input:str
    response:object


# ============================================================
# Node 1
# ============================================================

def agent_node(state):

    response = llm_tools.invoke(
        [
            HumanMessage(
                content=state["user_input"]
            )
        ]
    )

    return {
        "response":response
    }


# ============================================================
# Node 2
# ============================================================

def tool_node(state):

    global current_flight

    response=state["response"]

    if not response.tool_calls:

        return {
            "response":response.content
        }

    tool_call=response.tool_calls[0]

    name=tool_call["name"]
    args=tool_call["args"]

    # Search

    if name=="search_flights":

        result=search_flights.invoke(args)

        if "message" in result:

            return {
                "response":"No flights found"
            }

        current_flight=result

        return {

            "response":f"""
==================================================
Recommended Flight
==================================================

Flight ID : {result['flight_id']}
Airline   : {result['airline']}
Route     : {result['from']} → {result['to']}
Time      : {result['time']}
Price     : ₹{result['price']}

1. Generate New Flight
2. Book Current Flight
3. Cancel Flight
"""
        }


    # Book

    elif name=="book_flight":

        result=book_flight.invoke(args)

        return {

            "response":f"""
==================================================
Flight Confirmed
==================================================

Booking ID : {result['booking_id']}
Flight ID  : {result['flight_id']}
"""
        }


    # Cancel

    elif name=="cancel_flight":

        result=cancel_flight.invoke(args)

        return {

            "response":f"""
==================================================
Flight Cancelled
==================================================

Flight ID : {result['flight_id']}
"""
        }


# ============================================================
# Graph
# ============================================================

graph = StateGraph(
    AgentState
)

graph.add_node(
    "agent",
    agent_node
)

graph.add_node(
    "tool",
    tool_node
)

graph.set_entry_point(
    "agent"
)

graph.add_edge(
    "agent",
    "tool"
)

graph.add_edge(
    "tool",
    END
)

app = graph.compile()