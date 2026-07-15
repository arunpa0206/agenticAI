import random
from langchain.tools import tool

@tool
def search_hotels(city: str):
    """
    Search for hotels in a specific destination city.
    Returns a hotel option including hotel name, price per night, and rating.
    """
    hotel_names = [
        "Grand Palace Hotel",
        "Sunset Vista Resort",
        "Urban Elite Suites",
        "Cozy Corner Inn",
        "Royal Orchid Stay"
    ]
    selected_hotel = random.choice(hotel_names)
    price = random.randint(2000, 12000)
    rating = round(random.uniform(3.5, 4.9), 1)

    return {
        "hotel_name": selected_hotel,
        "city": city.strip().title(),
        "price_per_night": f"₹{price:,}",
        "rating": f"{rating}/5.0"
    }
