# ============================================================
# TOOL: SEARCH FLIGHT
# ============================================================

from langchain_core.tools import tool
from .state import conversation_state
from .search_agent import search_agent


@tool
def search_flight(source: str, destination: str) -> str:
    """
    Search for flights matching the source and destination.
    """
    # Track the route search parameters in the conversation context
    conversation_state["source"] = source
    conversation_state["destination"] = destination

    # Query the search sub-agent for search results
    flight = search_agent({
        "source": source,
        "destination": destination
    })
    conversation_state["current_flight"] = flight

    return (
        f"\nFlight Found\n"
        f"-------------------------\n"
        f"Flight ID : {flight['flight_id']}\n"
        f"Airline   : {flight['airline']}\n"
        f"Route     : {flight['source']} → {flight['destination']}\n"
        f"Departure : {flight['time']}\n"
        f"Price     : {flight['price']}\n"
        f"\nSay 'yes' to book or 'another' for a different flight."
    )
