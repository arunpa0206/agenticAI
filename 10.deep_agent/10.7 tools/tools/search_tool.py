# search_tool.py

import random
import json


def search_tool(travel_plan):

    print("=" * 60)
    print("SEARCH TOOL")
    print("=" * 60)

    required_fields = [
        "source",
        "destination"
    ]

    for field in required_fields:

        if field not in travel_plan:

            raise Exception(
                "Invalid Search Contract"
            )

    # Always overwrite plan.json
    plan_data = {
        "source":
        travel_plan["source"],

        "destination":
        travel_plan["destination"]
    }

    with open(
        "plan.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            plan_data,
            f,
            indent=4
        )

    airlines = [
        "IndiGo",
        "Air India",
        "SpiceJet",
        "Vistara",
        "Akasa Air"
    ]

    times = [
        "06:30 AM",
        "09:15 AM",
        "12:45 PM",
        "04:20 PM",
        "08:00 PM"
    ]

    prices = [
        "₹4200",
        "₹5100",
        "₹6200",
        "₹7400",
        "₹8500"
    ]

    selected_flight = {

        "flight_id":
        f"FL{random.randint(100,999)}",

        "airline":
        random.choice(
            airlines
        ),

        "time":
        random.choice(
            times
        ),

        "price":
        random.choice(
            prices
        ),

        "source":
        travel_plan["source"],

        "destination":
        travel_plan["destination"]
    }

    with open(
        "flight.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            selected_flight,
            f,
            indent=4,
            ensure_ascii=False
        )

    return selected_flight