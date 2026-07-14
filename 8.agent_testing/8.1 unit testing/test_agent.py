# test_agent.py

import unittest

# Import the agent nodes that we want to test
from langgraph_flow import (
    generate_flight,
    book_flight_node,
    cancel_flight_node
)


# Test class containing all unit tests
class TestFlightAgent(unittest.TestCase):

    # Test whether the generate_flight node returns flights
    def test_generate_flight(self):

        # Sample input state for the agent
        state = {
            "user_input": "Find a flight from Bangalore to Delhi",
            "intent": "search",
            "flights": [],
            "bookings": [],
            "response": ""
        }

        # Call the agent node
        result = generate_flight(state)

        # Verify that two flights are returned
        self.assertEqual(len(result["flights"]), 2)

    # Test whether the booking node creates bookings
    def test_book_flight(self):

        # Sample state containing available flights
        state = {
            "flights": [
                {"flight_id": "FL101"},
                {"flight_id": "FL102"},
            ],
            "bookings": [],
            "response": ""
        }

        # Call the booking node
        result = book_flight_node(state)

        # Verify that two bookings were created
        self.assertEqual(len(result["bookings"]), 2)

    # Test whether the cancel node clears all bookings and flights
    def test_cancel_flight(self):

        # Sample state with an existing booking
        state = {
            "flights": [
                {"flight_id": "FL101"}
            ],
            "bookings": [
                {"booking_id": "BK1000", "flight_id": "FL101"}
            ],
            "response": ""
        }

        # Call the cancel node
        result = cancel_flight_node(state)

        # Verify that bookings have been removed
        self.assertEqual(result["bookings"], [])

        # Verify that flights have also been cleared
        self.assertEqual(result["flights"], [])


# Runs all the tests when this file is executed
if __name__ == "__main__":
    unittest.main()