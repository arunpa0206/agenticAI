# ============================================================
# TOOL: ANOTHER FLIGHT
# ============================================================

from langchain_core.tools import tool
from .state import conversation_state
from .search_agent import search_agent


@tool
def another_flight() -> str:
    """
    Generate another flight for the current active route.
    """
    source = conversation_state["source"]
    destination = conversation_state["destination"]

    if source is None:
        return "No route available yet."

    # Query the search sub-agent again for an alternative flight
    flight = search_agent({
        "source": source,
        "destination": destination
    })
    conversation_state["current_flight"] = flight

    return (
        f"\nNew Flight Found\n"
        f"-------------------------\n"
        f"Flight ID : {flight['flight_id']}\n"
        f"Airline   : {flight['airline']}\n"
        f"Route     : {flight['source']} → {flight['destination']}\n"
        f"Departure : {flight['time']}\n"
        f"Price     : {flight['price']}\n"
        f"\nSay 'yes' to book or 'another' for another flight."
    )
