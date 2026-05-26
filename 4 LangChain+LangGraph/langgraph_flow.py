from typing import TypedDict

from langgraph.graph import StateGraph, END
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
    model="claude-sonnet-4-20250514",
    anthropic_api_key="YOUR_API_KEY",
    temperature=0
)

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

    user_input = state["user_input"]

    system_prompt = """
    You are an AI Flight Assistant.

    Rules:
    - Help users with flights
    - Use tools whenever needed
    - Never make up flights
    - Keep responses short
    """

    response = llm_with_tools.invoke([
        HumanMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ])

    # --------------------------------------------------------
    # TOOL CALLS
    # --------------------------------------------------------

    if response.tool_calls:

        final_output = ""

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # ------------------------------------------------
            # SEARCH FLIGHTS
            # ------------------------------------------------

            if tool_name == "search_flights":

                result = search_flights.invoke(tool_args)

                if isinstance(result, dict):

                    final_output = f"""
==================================================
Recommended Flight
==================================================

Flight ID   : {result['flight_id']}
Airline     : {result['airline']}
Route       : {result['from']} → {result['to']}
Departure   : {result['time']}
Price       : ₹{result['price']}

1. Confirm Flight
2. Generate New Flight Plan
3. Cancel Flight Plan
"""

                else:
                    final_output = result

            # ------------------------------------------------
            # BOOK FLIGHT
            # ------------------------------------------------

            elif tool_name == "book_flight":

                result = book_flight.invoke(tool_args)

                final_output = f"""
==================================================
Flight Confirmed
==================================================

Booking ID : {result['booking_id']}
Flight ID  : {result['flight_id']}

Your ticket has been booked successfully.
"""

            # ------------------------------------------------
            # CANCEL FLIGHT
            # ------------------------------------------------

            elif tool_name == "cancel_flight":

                result = cancel_flight.invoke(tool_args)

                final_output = f"""
==================================================
Flight Cancelled
==================================================

Flight ID : {result['flight_id']}

Your booking has been cancelled successfully.
"""

        return {
            "user_input": user_input,
            "response": final_output
        }

    return {
        "user_input": user_input,
        "response": response.content
    }

# ============================================================
# Build LangGraph
# ============================================================

graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)

graph.set_entry_point("agent")

graph.add_edge("agent", END)

app = graph.compile()