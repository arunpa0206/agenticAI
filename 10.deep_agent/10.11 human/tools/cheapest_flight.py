import random


def cheapest_flight_search():

    airlines=[

        "IndiGo",
        "SpiceJet",
        "Akasa Air"

    ]


    return {

        "flight_id":
        f"CF{random.randint(100,999)}",

        "type":
        "Cheapest Flight",

        "airline":
        random.choice(
            airlines
        ),

        "price":
        f"₹{random.randint(3000,6000)}"

    }