# search.py

import random
from langchain.tools import tool

flight_options = [

    {
        "flight_id": "AI101",
        "airline": "Air India",
        "price": "₹5200"
    },

    {
        "flight_id": "6E202",
        "airline": "IndiGo",
        "price": "₹4300"
    },

    {
        "flight_id": "UK303",
        "airline": "Vistara",
        "price": "₹7200"
    }
]


@tool
def search_flights():

    """
    Generate a flight option.
    """

    selected_flight = random.choice(
        flight_options
    )

    return f"""

Flight Details

Flight ID:
{selected_flight["flight_id"]}

Airline:
{selected_flight["airline"]}

Price:
{selected_flight["price"]}

Ask the user whether
they want to proceed
or generate another flight.

"""