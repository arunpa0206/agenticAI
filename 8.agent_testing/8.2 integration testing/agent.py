import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

import random

from tools import (
    search_flights,
    check_fare_rules,
    calculate_price,
    book_flight,
    cancel_booking
)


llm=ChatAnthropic(
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-5",

    temperature=0

)


tools=[

    search_flights,
    check_fare_rules,
    calculate_price,
    book_flight,
    cancel_booking

]

llm_with_tools=llm.bind_tools(
    tools
)



class FlightBookingAgent:

    def __init__(self):

        self.available_flights=[]
        self.selected_flight=None



    def plan_trip(
        self,
        user_query
    ):

        text=user_query.lower()

        source="Bangalore"
        destination="Delhi"

        try:

            words=text.split()

            if(
                "from" in words
                and
                "to" in words
            ):

                source=words[
                    words.index(
                        "from"
                    )+1
                ]

                destination=words[
                    words.index(
                        "to"
                    )+1
                ]

        except:

            pass



        result=search_flights.invoke({

            "source":
            source,

            "destination":
            destination

        })



        if not result:

            return """

============================================================
NO FLIGHTS FOUND
============================================================

No flights available for this route.

"""



        self.available_flights=[

            random.choice(
                result
            )

        ]

        flight=(
            self.available_flights[0]
        )



        return f"""

============================================================
AVAILABLE FLIGHT
============================================================

Flight ID      : {flight['flight_id']}
Airline        : {flight['airline']}
Route          : {flight['source']} → {flight['destination']}
Departure Time : {flight['departure_time']}
Price          : ₹{flight['price']}

"""



    def select_flight(
        self,
        index,
        passengers
    ):

        self.selected_flight=(
            self.available_flights[index]
        )


        fare_rules=check_fare_rules.invoke({

            "flight_id":
            self.selected_flight[
                "flight_id"
            ]

        })


        pricing=calculate_price.invoke({

            "base_price":
            self.selected_flight[
                "price"
            ],

            "passengers":
            passengers

        })


        return {

            "flight":
            self.selected_flight,

            "fare_rules":
            fare_rules,

            "pricing":
            pricing

        }



    def confirm_booking(self):

        return book_flight.invoke({

            "flight_id":
            self.selected_flight[
                "flight_id"
            ]

        })



    def cancel_current_booking(self):

        return cancel_booking.invoke({

            "flight_id":
            self.selected_flight[
                "flight_id"
            ]

        })