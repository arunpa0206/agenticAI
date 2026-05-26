import random


def premium_business_search():

    airlines=[

        "Air India",
        "Vistara",
        "Emirates"

    ]


    return {

        "flight_id":
        f"PB{random.randint(100,999)}",

        "type":
        "Premium Business Class",

        "airline":
        random.choice(
            airlines
        ),

        "price":
        f"₹{random.randint(15000,35000)}"

    }