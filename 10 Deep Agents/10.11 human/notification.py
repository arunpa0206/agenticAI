def notification_workflow(

    approved_flight,
    payment_status
):


    print("="*70)

    print(
        "FLIGHT TICKET"
    )

    print("="*70)


    print(

        f"\nFlight ID: "

        f"{approved_flight['flight_id']}"

    )

    print(

        f"Airline: "

        f"{approved_flight['airline']}"

    )

    print(

        f"Type: "

        f"{approved_flight['type']}"

    )

    print(

        f"Price: "

        f"{approved_flight['price']}"

    )

    print(

        f"Payment: "

        f"{payment_status['payment_status']}"

    )