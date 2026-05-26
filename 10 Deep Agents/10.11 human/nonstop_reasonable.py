import random


def nonstop_reasonable_search():

    airlines=[

        "Vistara",
        "Air India",
        "Akasa Air"

    ]


    return {

        "flight_id":
        f"NS{random.randint(100,999)}",

        "type":
        "Non-Stop Reasonable Price",

        "airline":
        random.choice(
            airlines
        ),

        "price":
        f"₹{random.randint(6000,12000)}"

    }