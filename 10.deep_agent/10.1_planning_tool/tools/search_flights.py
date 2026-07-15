import random
from langchain.tools import tool

@tool
def search_flights(source: str, destination: str):
    """
    Search for flights from a source city to a destination city.
    Returns details of a flight option including flight type, travel time, and price.
    """
    flight_types = ["Economy", "Business", "Premium Economy", "Budget Saver"]
    selected_type = random.choice(flight_types)
    price = random.randint(3000, 15000)
    travel_time = f"{random.randint(1, 4)}h {random.choice([0, 15, 30, 45])}m"

    return {
        "flight_id": f"FL-{random.randint(100, 999)}",
        "from": source.strip().title(),
        "to": destination.strip().title(),
        "flight_type": selected_type,
        "travel_time": travel_time,
        "price": f"₹{price:,}"
    }
