# cheapest_flight.py

import random
import time

def cheapest_flight_search(
    results
):

    time.sleep(1)

    results.append(
        {
            "flight_type":
            "Cheapest",

            "flight":
            f"6E{random.randint(100,999)}",

            "airline":
            "IndiGo",

            "price":
            f"₹{random.randint(3000,6000)}"
        }
    )