# search_worker.py

from langchain.tools import tool
import random


flights = [

    {
        "flight_id":"FL101",
        "from":"Bangalore",
        "to":"Delhi",
        "time":"6:30 PM",
        "price":"₹5200"
    },

    {
        "flight_id":"FL202",
        "from":"Bangalore",
        "to":"Delhi",
        "time":"8:15 PM",
        "price":"₹6100"
    },

    {
        "flight_id":"FL303",
        "from":"Delhi",
        "to":"Mumbai",
        "time":"9:00 AM",
        "price":"₹4500"
    }
]


previous = None


@tool
def search_worker(
    source: str,
    destination: str
):
    """
    Search for flights between
    source and destination.
    """

    global previous

    results = [

        flight

        for flight in flights

        if (

            flight["from"].lower()
            ==
            source.lower()

            and

            flight["to"].lower()
            ==
            destination.lower()

        )
    ]


    if len(results) == 0:

        return "No flights found"


    available = [

        flight

        for flight in results

        if flight != previous
    ]


    if len(available) == 0:

        available = results


    selected = random.choice(
        available
    )

    previous = selected


    return f"""

Flight Details

Flight ID:
{selected["flight_id"]}

Route:
{selected["from"]} → {selected["to"]}

Time:
{selected["time"]}

Price:
{selected["price"]}

Would you like to continue
with booking or see
another flight?

"""