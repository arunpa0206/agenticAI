import unittest

from agent import FlightBookingAgent

# ============================================================
# UNIT TESTING
# ============================================================

class TestFlightBooking(unittest.TestCase):

    # ========================================================
    # TEST SEARCH
    # ========================================================

    def test_flight_search(self):

        agent = FlightBookingAgent()

        result = agent.plan_trip(
            "Book a flight from Bangalore to Delhi"
        )

        self.assertIn(
            "AVAILABLE FLIGHT",
            result
        )

    # ========================================================
    # TEST BOOKING
    # ========================================================

    def test_booking_confirmation(self):

        agent = FlightBookingAgent()

        agent.plan_trip(
            "Book a flight from Bangalore to Delhi"
        )

        agent.select_flight(
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