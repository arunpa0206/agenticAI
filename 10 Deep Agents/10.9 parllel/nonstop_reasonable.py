# nonstop_reasonable.py

import random
import time

def nonstop_reasonable_search(
    results
):

    time.sleep(1)

    results.append(
        {
            "flight_type":
            "Nonstop",

            "flight":
            f"UK{random.randint(100,999)}",

            "airline":
            "Vistara",

            "price":
            f"₹{random.randint(6000,9000)}"
        }
    )