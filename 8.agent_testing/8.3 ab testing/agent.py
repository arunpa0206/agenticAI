import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from tools import search_flights, book_flight

import random


llm = ChatAnthropic(
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-5",

)


class FlightBookingAgent:

    def __init__(self):

        self.selected_flight=None


    def plan_trip(
        self,
        user_query,
        strategy="A"
    ):

        llm.invoke([

            HumanMessage(
                content=user_query
            )

        ])


        flights=search_flights.invoke({

            "source":"Bangalore",
            "destination":"Delhi"

        })


        # ==========================================
        # VERSION A
        # Cheapest flight
        # ==========================================

        if strategy=="A":

            self.selected_flight=min(

                flights,
                key=lambda x:x["price"]

            )

            version="A VERSION - CHEAPEST FLIGHT"


        # ==========================================
        # VERSION B
        # Random flight
        # ==========================================

        else:

            self.selected_flight=random.choice(
                flights
            )

            version="B VERSION - RANDOM FLIGHT"



        flight=self.selected_flight


        return f"""
============================================================
{version}
============================================================

Flight ID      : {flight['flight_id']}
Airline        : {flight['airline']}
Route          : {flight['source']} → {flight['destination']}
Departure Time : {flight['departure_time']}
Price          : ₹{flight['price']}
"""


    def confirm_booking(self):

        return book_flight.invoke({

            "flight_id":
            self.selected_flight["flight_id"]

        })