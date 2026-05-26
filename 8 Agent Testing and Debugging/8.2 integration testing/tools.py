import random
import uuid
import difflib

from langchain_core.tools import tool

# ============================================================
# FLIGHT DATABASE
# ============================================================

FLIGHT_DATABASE = [

    {
        "flight_id":"FL101",
        "airline":"IndiGo",
        "source":"Bangalore",
        "destination":"Delhi"
    },

    {
        "flight_id":"FL202",
        "airline":"Air India",
        "source":"Bangalore",
        "destination":"Delhi"
    },

    {
        "flight_id":"FL303",
        "airline":"Vistara",
        "source":"Bangalore",
        "destination":"Delhi"
    }

]


# ============================================================
# NORMALIZE CITY
# ============================================================

def normalize(city):

    city=city.lower().strip()

    cities=[

        "bangalore",
        "delhi"

    ]

    match=difflib.get_close_matches(

        city,
        cities,
        n=1,
        cutoff=0.6

    )

    if match:

        return match[0]

    return city


# ============================================================
# SEARCH FLIGHTS
# ============================================================

@tool
def search_flights(
    source:str,
    destination:str
):
    """
    Search flights between cities.
    """

    source=normalize(source)
    destination=normalize(destination)

    results=[]

    for flight in FLIGHT_DATABASE:

        db_source=normalize(
            flight["source"]
        )

        db_destination=normalize(
            flight["destination"]
        )


        if (

            source==db_source
            and
            destination==db_destination

        ):

            generated={

                "flight_id":
                flight["flight_id"],

                "airline":
                flight["airline"],

                "source":
                flight["source"],

                "destination":
                flight["destination"],

                "departure_time":
                f"{random.randint(1,12)}:{random.choice(['00','15','30','45'])} {'AM' if random.randint(0,1)==0 else 'PM'}",

                "price":
                random.randint(
                    4000,
                    9000
                )

            }

            results.append(
                generated
            )

    return results


@tool
def check_fare_rules(
    flight_id:str
):
    """
    Check fare rules.
    """

    return {

        "flight_id":
        flight_id,

        "refundable":
        random.choice(
            [True,False]
        ),

        "cancellation_fee":
        random.randint(
            500,
            2000
        )

    }


@tool
def calculate_price(
    base_price:int,
    passengers:int
):
    """
    Calculate total ticket price.
    """

    taxes=int(
        base_price*0.18
    )

    total=(
        base_price+taxes
    )*passengers

    return {

        "base_price":
        base_price,

        "taxes":
        taxes,

        "passengers":
        passengers,

        "total_price":
        total

    }


@tool
def book_flight(
    flight_id:str
):
    """
    Confirm booking.
    """

    return {

        "booking_id":
        str(uuid.uuid4())[:8],

        "flight_id":
        flight_id,

        "status":
        "CONFIRMED"

    }


@tool
def cancel_booking(
    flight_id:str
):
    """
    Cancel booking.
    """

    return {

        "flight_id":
        flight_id,

        "status":
        "CANCELLED"

    }