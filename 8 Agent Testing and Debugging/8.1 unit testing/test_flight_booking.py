import unittest

from agent import FlightBookingAgent

# ============================================================
# UNIT TESTS
# ============================================================

class TestFlightBooking(unittest.TestCase):

    # --------------------------------------------------------
    # TEST 1: FLIGHT SEARCH
    # --------------------------------------------------------

    def test_flight_search(self):

        agent = FlightBookingAgent()

        result = agent.plan_trip(
            "Book a flight from Bangalore to Delhi"
        )

        self.assertIn(
            "AVAILABLE FLIGHT",
            result
        )

    # --------------------------------------------------------
    # TEST 2: INVALID ROUTE
    # --------------------------------------------------------

    def test_invalid_route(self):

        agent = FlightBookingAgent()

        result = agent.plan_trip(
            "Book a flight from Delhi to Delhi"
        )

        self.assertIsNotNone(result)

    # --------------------------------------------------------
    # TEST 3: BOOKING CONFIRMATION
    # --------------------------------------------------------

    def test_booking_confirmation(self):

        agent = FlightBookingAgent()

        agent.plan_trip(
            "Book a flight from Bangalore to Delhi"
        )

        selected = agent.select_flight(
            index=0,
            passengers=1
        )

        booking = agent.confirm_booking()

        self.assertEqual(
            booking["status"],
            "CONFIRMED"
        )

# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":

    unittest.main()