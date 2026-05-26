import unittest

from agent import FlightBookingAgent


class TestABTesting(unittest.TestCase):


    def test_version_a(self):

        agent=FlightBookingAgent()

        result=agent.plan_trip(

            "Book a flight from Bangalore to Delhi",
            strategy="A"

        )

        self.assertIn(

            "A VERSION",
            result

        )


    def test_version_b(self):

        agent=FlightBookingAgent()

        result=agent.plan_trip(

            "Book a flight from Bangalore to Delhi",
            strategy="B"

        )

        self.assertIn(

            "B VERSION",
            result

        )


    def test_ab_difference(self):

        agent=FlightBookingAgent()

        result_a=agent.plan_trip(

            "Book a flight from Bangalore to Delhi",
            strategy="A"

        )


        result_b=agent.plan_trip(

            "Book a flight from Bangalore to Delhi",
            strategy="B"

        )


        self.assertNotEqual(
            result_a,
            result_b
        )


if __name__=="__main__":

    unittest.main()