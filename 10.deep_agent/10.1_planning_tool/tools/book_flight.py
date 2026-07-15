import random
from langchain.tools import tool

@tool
def book_flight(flight_id: str, passenger_name: str):
    """
    Confirms and books a flight using the flight ID and the passenger's name.
    Returns a confirmed booking record containing a unique Booking ID.
    """
    booking_id = f"BK-{random.randint(5000, 9999)}"
    return {
        "booking_id": booking_id,
        "flight_id": flight_id,
        "passenger_name": passenger_name.strip().title(),
        "status": "Confirmed"
    }
