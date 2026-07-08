# premium_business.py

import random
import time

def premium_business_search(
    results
):

    time.sleep(1)

    results.append(
        {
            "flight_type":
            "Premium Business",

            "flight":
            f"AI{random.randint(100,999)}",

            "airline":
            "Air India",

            "price":
            f"₹{random.randint(15000,22000)}"
        }
    )