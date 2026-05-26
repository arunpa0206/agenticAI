from agent import FlightBookingAgent
import unittest
import test_flight_booking

# ============================================================
# INITIALIZE AGENT
# ============================================================

agent = FlightBookingAgent()

# ============================================================
# USER INPUT
# ============================================================

query = input(
    "\nWhere would you like to travel?\n\nYou: "
)

# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # --------------------------------------------------------
    # GENERATE FLIGHT
    # --------------------------------------------------------

    response = agent.plan_trip(query)

    print(response)

    # --------------------------------------------------------
    # OPTIONS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("OPTIONS")
    print("=" * 60)

    print("1. Confirm Booking")
    print("2. Generate New Flight")
    print("3. Cancel Booking")

    option = input("\nEnter Option Number: ")

    # ========================================================
    # OPTION 1 = CONFIRM BOOKING
    # ========================================================

    if option == "1":

        selected = agent.select_flight(
            index=0,
            passengers=1
        )

        flight = selected["flight"]
        fare_rules = selected["fare_rules"]
        pricing = selected["pricing"]

        print("\n" + "=" * 60)
        print("SELECTED FLIGHT DETAILS")
        print("=" * 60)

        print(f"\nFlight ID          : {flight['flight_id']}")
        print(f"Airline            : {flight['airline']}")
        print(f"Route              : {flight['source']} → {flight['destination']}")
        print(f"Departure Time     : {flight['departure_time']}")

        print("\nFare Rules")
        print("-" * 40)

        print(f"Refundable         : {fare_rules['refundable']}")
        print(f"Cancellation Fee   : ₹{fare_rules['cancellation_fee']}")

        print("\nPricing")
        print("-" * 40)

        print(f"Base Price         : ₹{pricing['base_price']}")
        print(f"Taxes              : ₹{pricing['taxes']}")
        print(f"Passengers         : {pricing['passengers']}")
        print(f"Total Price        : ₹{pricing['total_price']}")

        booking = agent.confirm_booking()

        print("\n" + "=" * 60)
        print("BOOKING CONFIRMED")
        print("=" * 60)

        print(f"\nBooking ID : {booking['booking_id']}")
        print(f"Flight ID  : {booking['flight_id']}")
        print(f"Status     : {booking['status']}")

        break

    # ========================================================
    # OPTION 2 = GENERATE NEW FLIGHT
    # ========================================================

    elif option == "2":

        print("\nGenerating Another Flight...\n")

        continue

    # ========================================================
    # OPTION 3 = CANCEL
    # ========================================================

    elif option == "3":

        print("\nBooking Cancelled.")

        break

    # ========================================================
    # INVALID OPTION
    # ========================================================

    else:

        print("\nInvalid Option. Please choose 1, 2, or 3.")

# ============================================================
# RUN UNIT TESTS
# ============================================================

print("\n" + "=" * 60)
print("RUNNING UNIT TESTS")
print("=" * 60)

suite = unittest.defaultTestLoader.loadTestsFromModule(
    test_flight_booking
)

runner = unittest.TextTestRunner()

runner.run(suite)