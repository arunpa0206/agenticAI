from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from tools import (
    search_flights,
    check_fare_rules,
    calculate_price,
    book_flight,
    cancel_booking
)

# ============================================================
# CLAUDE LLM
# ============================================================

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    anthropic_api_key="YOUR_API_KEY",
    temperature=0
)

# ============================================================
# BIND TOOLS
# ============================================================

tools = [
    search_flights,
    check_fare_rules,
    calculate_price,
    book_flight,
    cancel_booking
]

llm_with_tools = llm.bind_tools(tools)

# ============================================================
# FLIGHT BOOKING AGENT
# ============================================================

class FlightBookingAgent:

    def __init__(self):

        self.available_flights = []
        self.selected_flight = None

    # ========================================================
    # PLAN TRIP
    # ========================================================

    def plan_trip(self, user_query):

        response = llm_with_tools.invoke([
            HumanMessage(content=user_query)
        ])

        final_response = ""

        # ----------------------------------------------------
        # TOOL CALLS
        # ----------------------------------------------------

        if response.tool_calls:

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                # ------------------------------------------------
                # SEARCH FLIGHTS
                # ------------------------------------------------

                if tool_name == "search_flights":

                    result = search_flights.invoke(tool_args)

                    # ONLY ONE FLIGHT
                    self.available_flights = [result[0]]

                    flight = result[0]

                    final_response += f"""

============================================================
AVAILABLE FLIGHT
============================================================

Flight ID      : {flight['flight_id']}
Airline        : {flight['airline']}
Route          : {flight['source']} → {flight['destination']}
Departure Time : {flight['departure_time']}
Price          : ₹{flight['price']}
"""

        else:

            final_response = """
From where would you like to travel?

Example:
Book a flight from Bangalore to Delhi
"""

        return final_response

    # ========================================================
    # SELECT FLIGHT
    # ========================================================

    def select_flight(self, index, passengers):

        self.selected_flight = self.available_flights[index]

        fare_rules = check_fare_rules.invoke({
            "flight_id": self.selected_flight["flight_id"]
        })

        pricing = calculate_price.invoke({
            "base_price": self.selected_flight["price"],
            "passengers": passengers
        })

        return {
            "flight": self.selected_flight,
            "fare_rules": fare_rules,
            "pricing": pricing
        }

    # ========================================================
    # CONFIRM BOOKING
    # ========================================================

    def confirm_booking(self):

        return book_flight.invoke({
            "flight_id": self.selected_flight["flight_id"]
        })

    # ========================================================
    # CANCEL BOOKING
    # ========================================================

    def cancel_current_booking(self):

        return cancel_booking.invoke({
            "flight_id": self.selected_flight["flight_id"]
        })