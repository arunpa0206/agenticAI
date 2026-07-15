import random
import time
from langchain_core.tools import tool
from .error_handler import handle_error
from .notification_agent import failure_notification
from .state import conversation_state

@tool
def search_flight(source: str, destination: str) -> str:
    """
    Search one flight only
    """
    current_time = int(time.time())

    try:
        # Simulate random system failure
        if current_time % 2 == 0:
            raise Exception("Flight search system failure")

    except Exception:
        retry = handle_error()
        if not retry:
            failure_notification()
            return "Search unavailable."

    airlines = ["Air India", "IndiGo", "SpiceJet", "Vistara"]
    times = ["06:30 AM", "09:15 AM", "12:45 PM", "04:20 PM"]
    prices = ["₹5200", "₹6100", "₹7300", "₹8500"]

    flight = {
        "flight_id": f"FL{random.randint(100, 999)}",
        "airline": random.choice(airlines),
        "time": random.choice(times),
        "price": random.choice(prices),
        "source": source,
        "destination": destination
    }

    conversation_state["source"] = source
    conversation_state["destination"] = destination
    conversation_state["current_flight"] = flight

    return (
        f"\nFlight Found\n"
        f"------------------\n"
        f"Flight ID : {flight['flight_id']}\n"
        f"Airline   : {flight['airline']}\n"
        f"Route     : {source} → {destination}\n"
        f"Time      : {flight['time']}\n"
        f"Price     : {flight['price']}\n"
        f"\nType:\n"
        f"- yes\n"
        f"- another"
    )
