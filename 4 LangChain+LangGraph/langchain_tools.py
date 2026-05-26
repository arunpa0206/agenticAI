import random
from langchain_core.tools import tool

# ============================================================
# Mock Flight Database
# ============================================================

flights = [
    {
        "flight_id": "FL101",
        "airline": "IndiGo",
        "from": "Bangalore",
        "to": "Delhi",
        "time": "6:30 PM",
        "price": 5200
    },
    {
        "flight_id": "FL202",
        "airline": "Air India",
        "from": "Bangalore",
        "to": "Delhi",
        "time": "8:15 PM",
        "price": 6100
    },
    {
        "flight_id": "FL303",
        "airline": "Vistara",
        "from": "Bangalore",
        "to": "Delhi",
        "time": "9:45 PM",
        "price": 5700
    }
]

# ============================================================
# Search Flights Tool
# ============================================================

@tool
def search_flights(source: str, destination: str):
    """
    Search available flights.
    """

    results = []

    for flight in flights:

        if (
            flight["from"].lower() == source.lower()
            and flight["to"].lower() == destination.lower()
        ):
            results.append(flight)

    if not results:
        return "No flights found."

    return random.choice(results)

# ============================================================
# Book Flight Tool
# ============================================================

@tool
def book_flight(flight_id: str):
    """
    Confirm flight booking.
    """

    return {
        "status": "CONFIRMED",
        "booking_id": "BK78291",
        "flight_id": flight_id
    }

# ============================================================
# Cancel Flight Tool
# ============================================================

@tool
def cancel_flight(flight_id: str):
    """
    Cancel booked flight.
    """

    return {
        "status": "CANCELLED",
        "flight_id": flight_id
    }