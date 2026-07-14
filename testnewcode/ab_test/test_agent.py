# ab_test.py

import unittest
from langgraph_flow import generate_flight


# -----------------------------
# Version A (Current Agent)
# -----------------------------
def version_a(state):
    return generate_flight(state)


# -----------------------------
# Version B (Improved Agent)
# Adds an extra direct flight
# -----------------------------
def version_b(state):

    # Generate the normal flights first
    result = generate_flight(state)

    # Add an additional direct flight
    result["flights"].append(
        {
            "flight_id": "FL103",
            "from": "Bangalore",
            "to": "Delhi",
            "time": "7:00 PM",
            "price": 3900
        }
    )

    # Update the response shown to the user
    result["response"] += (
        "\nFL103: Bangalore -> Delhi ₹3900"
    )

    return result


# -----------------------------
# A/B Tests
# -----------------------------
class TestFlightAgentAB(unittest.TestCase):

    # Compare the search results of Version A and Version B
    def test_search_ab(self):

        state = {
            "user_input": "Find a flight from Bangalore to Delhi",
            "intent": "search",
            "flights": [],
            "bookings": [],
            "response": ""
        }

        # Run Version A
        result_a = version_a(state)

        # Run Version B
        result_b = version_b(state)

        # Version A should return 2 flights
        self.assertEqual(len(result_a["flights"]), 2)

        # Version B should return 3 flights
        self.assertEqual(len(result_b["flights"]), 3)

        # Version B should have more flight options
        self.assertGreater(
            len(result_b["flights"]),
            len(result_a["flights"])
        )

        # Version B should contain the new flight
        self.assertIn("FL103", result_b["response"])


if __name__ == "__main__":
    unittest.main()