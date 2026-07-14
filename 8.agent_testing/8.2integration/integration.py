# integration_test.py

import unittest
from langgraph_flow import app


class TestFlightAgentIntegration(unittest.TestCase):

    # Test the complete search flow
    def test_search_flow(self):

        state = {
            "user_input": "Find a flight from Bangalore to Delhi",
            "intent": "",
            "flights": [],
            "bookings": [],
            "response": ""
        }

        # Run the complete agent
        result = app.invoke(state)

        # Verify that flights were generated
        self.assertEqual(len(result["flights"]), 2)

    # Test the complete booking flow
    def test_booking_flow(self):

        state = {
            "user_input": "Book these flights",
            "intent": "book",
            "flights": [
                {"flight_id": "FL101"},
                {"flight_id": "FL102"}
            ],
            "bookings": [],
            "response": ""
        }

        # Run the complete agent
        result = app.invoke(state)

        # Verify that bookings were created
        self.assertEqual(len(result["bookings"]), 2)


if __name__ == "__main__":
    unittest.main()