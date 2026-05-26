from agent import FlightBookingAgent
import unittest
import test_ab_testing

agent=FlightBookingAgent()

query=input(
"\nWhere would you like to travel?\n\nYou: "
)


result_a=agent.plan_trip(
    query,
    strategy="A"
)

print(result_a)


result_b=agent.plan_trip(
    query,
    strategy="B"
)

print(result_b)


print("\n"+"="*60)
print("RUNNING A/B TESTS")
print("="*60)


suite=unittest.defaultTestLoader.loadTestsFromModule(
    test_ab_testing
)

runner=unittest.TextTestRunner()

runner.run(
    suite
)