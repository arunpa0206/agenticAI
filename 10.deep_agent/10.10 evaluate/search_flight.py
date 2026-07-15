# ============================================================
# TOOL: SEARCH FLIGHT
# ============================================================

import time
import random
from langchain_core.tools import tool
from state import conversation_state


@tool
def search_flight(source: str, destination: str) -> str:
    """
    Generate one flight option matching the source and destination.
    """
    conversation_state["source"] = source
    conversation_state["destination"] = destination
    conversation_state["start_time"] = time.time()

    flight = {
        "flight_id": f"FL{random.randint(100, 999)}",
        "from": source,
        "to": destination,
        "time": random.choice(["6:30 PM", "8:15 PM", "10:45 PM"]),
        "price": random.choice(["₹4800", "₹5200", "₹6100"])
    }

    conversation_state["current_flight"] = flight

    return (
        f"\nFlight Found\n"
        f"----------------------\n"
        f"Flight : {flight['flight_id']}\n"
        f"Route : {flight['from']} → {flight['to']}\n"
        f"Time : {flight['time']}\n"
        f"Price : {flight['price']}\n\n"
        f"Type:\n"
        f"- yes\n"
        f"- another"
    )
