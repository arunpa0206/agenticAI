import unittest
from agent import FlightBookingAgent

# ============================================================
# INTEGRATION TESTING (LLM RESPONSE + WORKFLOW)
# ============================================================

class TestFlightBookingIntegration(unittest.TestCase):

    # ========================================================
    # TEST LLM GENERATED RESPONSE
    # ========================================================

    def test_llm_response_contains_flight(self):

        agent = FlightBookingAgent()

        response = agent.plan_trip(
            "Book a flight from Bangalore to Delhi"
        )

        self.assertIsNotNone(
            response
        )

        self.assertIn(
            "AVAILABLE FLIGHT",
            response
        )

        self.assertIn(
            "Flight ID",
            response
        )

        self.assertIn(
            "Airline",
            response
        )

        self.assertIn(
            "Route",
            response
        )


    # ========================================================
    # TEST COMPLETE END TO END FLOW
    # ========================================================

    def test_complete_booking_flow(self):

        agent = FlightBookingAgent()

        response = agent.plan_trip(
            "Book a flight from Bangalore to Delhi"
        )

        self.assertIn(
            "AVAILABLE FLIGHT",
            response
        )


        selected = agent.select_flight(
            index=0,
            passengers=1
        )


        self.assertIn(
            "flight",
            selected
        )

        self.assertIn(
            "pricing",
            selected
        )

        self.assertIn(
            "fare_rules",
            selected
        )


        booking = agent.confirm_booking()

        self.assertEqual(
            booking["status"],
            "CONFIRMED"
        )

        self.assertIsNotNone(
            booking["booking_id"]
        )


    # ========================================================
    # TEST CANCELLATION FLOW
    # ========================================================

    def test_booking_cancellation(self):

        agent = FlightBookingAgent()

        agent.plan_trip(
            "Book a flight from Bangalore to Delhi"
        )

        agent.select_flight(
            index=0,
            passengers=1
        )

        cancelled=agent.cancel_current_booking()

        self.assertEqual(
            cancelled["status"],
            "CANCELLED"
        )


    # ========================================================
    # TEST LLM RESPONSE CONSISTENCY
    # ========================================================

    def test_response_consistency(self):

        agent=FlightBookingAgent()

        for i in range(5):

            response=agent.plan_trip(
                "Book a flight from Bangalore to Delhi"
            )

            self.assertIn(
                "AVAILABLE FLIGHT",
                response
            )

            self.assertIn(
                "Price",
                response
            )


    # ========================================================
    # TEST LLM RELEVANCE
    # ========================================================

    def test_response_relevance(self):

        agent=FlightBookingAgent()

        response=agent.plan_trip(
            "I want to travel from Bangalore to Delhi"
        )

        keywords=[

            "Flight",
            "Airline",
            "Route",
            "Price"

        ]

        relevance=0

        for word in keywords:

            if word in response:

                relevance+=1


        score=(
            relevance/
            len(keywords)
        )*100


        self.assertGreaterEqual(
            score,
            75
        )


# ============================================================
# RUN
# ============================================================

if __name__=="__main__":

    unittest.main()