from typing import TypedDict

from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from langchain_tools import (
    search_flights,
    book_flight,
    cancel_flight
)

# ============================================================
# Claude Configuration
# ============================================================

llm = ChatAnthropic(
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-5",
    temperature=0
)

# ============================================================
# Store Current Flight
# ============================================================

current_flight = None

# ============================================================
# Bind Tools
# ============================================================

tools = [
    search_flights,
    book_flight,
    cancel_flight
]

llm_with_tools = llm.bind_tools(tools)

# ============================================================
# Agent State
# ============================================================

class AgentState(TypedDict):

    user_input: str
    response: str

# ============================================================
# Agent Node
# ============================================================

def agent_node(state: AgentState):

    global current_flight

    prompt = state["user_input"]

    # --------------------------------------------------------
    # Give Claude conversation context
    # --------------------------------------------------------

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

User Request:

{state["user_input"]}

Instructions:

- If the user says:
  "Book this flight"
  "Book it"

  use book_flight() with the current flight_id.

- If the user says:
  "Cancel this flight"
  "Cancel it"

  use cancel_flight() with the current flight_id.

- If the user says:
  "Generate another flight"
  "Another flight"
  "Show another flight"

  call search_flights() using the SAME source and destination
  as the current flight.

- Otherwise decide which tool should be used.
"""

    # --------------------------------------------------------
    # Ask Claude
    # --------------------------------------------------------

    response = llm_with_tools.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    # --------------------------------------------------------
    # No Tool Needed
    # --------------------------------------------------------

    if not response.tool_calls:

        return {

            "user_input": state["user_input"],

            "response": response.content

        }

    # --------------------------------------------------------
    # Read Tool Call
    # --------------------------------------------------------

    tool_call = response.tool_calls[0]

    tool_name = tool_call["name"]

    tool_args = tool_call["args"]

    # --------------------------------------------------------
    # Search Flights
    # --------------------------------------------------------

    if tool_name == "search_flights":

        result = search_flights.invoke(tool_args)

        current_flight = result

        return {

            "user_input": state["user_input"],

            "response": f"""

==================================================
Recommended Flight
==================================================

Flight ID : {result['flight_id']}
Airline   : {result['airline']}
Route     : {result['from']} → {result['to']}
Departure : {result['time']}
Price     : ₹{result['price']}

You can now say:

• Book this flight
• Generate another flight
• Cancel this flight

"""

        }

    # --------------------------------------------------------
    # Book Flight
    # --------------------------------------------------------

    elif tool_name == "book_flight":

        result = book_flight.invoke(tool_args)

        return {

            "user_input": state["user_input"],

            "response": f"""

==================================================
Flight Confirmed
==================================================

Booking ID : {result['booking_id']}
Flight ID  : {result['flight_id']}

Your booking has been confirmed.

"""

        }

    # --------------------------------------------------------
    # Cancel Flight
    # --------------------------------------------------------

    elif tool_name == "cancel_flight":

        result = cancel_flight.invoke(tool_args)

        return {

            "user_input": state["user_input"],

            "response": f"""

==================================================
Flight Cancelled
==================================================

Flight ID : {result['flight_id']}

Your booking has been cancelled.

"""

        }

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    return {

        "user_input": state["user_input"],

        "response": "Sorry, I couldn't process your request."

    }

# ============================================================
# Build LangGraph
# ============================================================

graph = StateGraph(AgentState)

graph.add_node(
    "agent",
    agent_node
)

graph.set_entry_point(
    "agent"
)

graph.add_edge(
    "agent",
    END
)

app = graph.compile()