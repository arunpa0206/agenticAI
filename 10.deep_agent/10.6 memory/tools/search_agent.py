# search_agent.py
# Search Agent

import random


def search_agent(search_context):

    print("\n" + "=" * 60)
    print("SEARCH AGENT")
    print("=" * 60)

    airlines = [
        "IndiGo",
        "Air India",
        "Akasa Air",
        "SpiceJet",
        "Vistara"
    ]

    timings = [
        "06:30 AM",
        "09:15 AM",
        "12:45 PM",
        "04:20 PM",
        "08:00 PM"
    ]

    prices = [
        "₹4200",
        "₹5100",
        "₹6300",
        "₹7200",
        "₹8500"
    ]

    flight = {

        "flight_id":
        f"FL{random.randint(100,999)}",

        "airline":
        random.choice(
            airlines
        ),

        "time":
        random.choice(
            timings
        ),

        "price":
        random.choice(
            prices
        ),

        "source":
        search_context["source"],

        "destination":
        search_context["destination"]
    }

    return flight