import random
import uuid

from langchain_core.tools import tool

# ============================================================
# FLIGHT DATABASE
# ============================================================

FLIGHT_DATABASE = [
    {
        "flight_id": "FL101",
        "airline": "IndiGo",
        "source": "Bangalore",
        "destination": "Delhi"
    },
    {
        "flight_id": "FL202",
        "airline": "Air India",
        "source": "Bangalore",
        "destination": "Delhi"
    },
    {
        "flight_id": "FL303",
        "airline": "Vistara",
        "source": "Bangalore",
        "destination": "Delhi"
    }
]

# ============================================================
# SEARCH FLIGHTS
# ============================================================

@tool
def search_flights(source: str, destination: str):
    """
    Search flights between source and destination.
    """

    results = []

    for flight in FLIGHT_DATABASE:

        if (
            flight["source"].lower() == source.lower()
            and flight["destination"].lower() == destination.lower()
        ):

            generated_flight = {
                "flight_id": flight["flight_id"],
                "airline": flight["airline"],
                "source": source,
                "destination": destination,
                "departure_time": f"{random.randint(1,12)}:{random.choice(['00','15','30','45'])} {'AM' if random.randint(0,1)==0 else 'PM'}",
                "price": random.randint(4000, 9000)
            }

            results.append(generated_flight)

    return results

# ============================================================
# BOOK FLIGHT
# ============================================================

@tool
def book_flight(flight_id: str):
    """
    Confirm flight booking.
    """

    return {
        "booking_id": str(uuid.uuid4())[:8],
        "flight_id": flight_id,
        "status": "CONFIRMED"
    }