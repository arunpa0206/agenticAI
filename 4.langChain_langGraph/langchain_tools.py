import random
from langchain_core.tools import tool

# ============================================================
# Mock Airlines
# ============================================================

AIRLINES = [
    "IndiGo",
    "Air India",
    "Vistara",
    "Emirates",
    "Qatar Airways",
    "Singapore Airlines",
    "Lufthansa",
    "British Airways",
    "Delta Airlines",
    "United Airlines"
]

# ============================================================
# Search Flights Tool
# ============================================================

@tool
def search_flights(source: str, destination: str):
    """
    Generate a realistic mock flight between any two cities.
    """

    return {

        "flight_id": f"FL{random.randint(100,999)}",

        "airline": random.choice(AIRLINES),

        "from": source.title(),

        "to": destination.title(),

        "time": (
            f"{random.randint(1,12)}:"
            f"{random.choice(['00','15','30','45'])} "
            f"{random.choice(['AM','PM'])}"
        ),

        "price": random.randint(3500, 85000)

    }


# ============================================================
# Book Flight Tool
# ============================================================

@tool
def book_flight(flight_id: str):
    """
    Book a flight.
    """

    return {

        "status": "CONFIRMED",

        "booking_id": f"BK{random.randint(1000,9999)}",

        "flight_id": flight_id

    }


# ============================================================
# Cancel Flight Tool
# ============================================================

@tool
def cancel_flight(flight_id: str):
    """
    Cancel a booked flight.
    """

    return {

        "status": "CANCELLED",

        "flight_id": flight_id

    }