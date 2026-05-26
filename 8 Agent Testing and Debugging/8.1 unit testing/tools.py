import random
import uuid
from langchain_core.tools import tool

# ============================================================
# Flight Database
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
# TOOL 1: Validate Input
# ============================================================

@tool
def validate_input(
    source: str,
    destination: str,
    departure_date: str,
    return_date: str,
    passengers: int,
    travel_class: str,
    non_stop: bool
):
    """
    Validate flight booking input.
    """

    if source == destination:

        return {
            "valid": False,
            "message": "Source and destination cannot be same."
        }

    if passengers <= 0:

        return {
            "valid": False,
            "message": "Passengers must be greater than zero."
        }

    return {
        "valid": True,
        "message": "Validation successful."
    }

# ============================================================
# TOOL 2: Search Flights
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
# TOOL 3: Check Fare Rules
# ============================================================

@tool
def check_fare_rules(flight_id: str):
    """
    Check fare rules for a flight.
    """

    return {
        "flight_id": flight_id,
        "refundable": random.choice([True, False]),
        "cancellation_fee": random.randint(500, 2000)
    }

# ============================================================
# TOOL 4: Calculate Price
# ============================================================

@tool
def calculate_price(base_price: int, passengers: int):
    """
    Calculate total ticket price.
    """

    taxes = int(base_price * 0.18)

    total_price = (base_price + taxes) * passengers

    return {
        "base_price": base_price,
        "taxes": taxes,
        "passengers": passengers,
        "total_price": total_price
    }

# ============================================================
# TOOL 5: Book Flight
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

# ============================================================
# TOOL 6: Cancel Booking
# ============================================================

@tool
def cancel_booking(flight_id: str):
    """
    Cancel flight booking.
    """

    return {
        "flight_id": flight_id,
        "status": "CANCELLED"
    }