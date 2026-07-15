# ============================================================
# TOOL: ANOTHER FLIGHT
# ============================================================

from langchain_core.tools import tool
from state import conversation_state
from search_flight import search_flight


@tool
def another_flight() -> str:
    """
    Replace the current flight option with a new search for the same route.
    """
    return search_flight.invoke({
        "source": conversation_state["source"],
        "destination": conversation_state["destination"]
    })
