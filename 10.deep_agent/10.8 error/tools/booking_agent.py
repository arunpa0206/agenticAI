# booking_agent.py

def booking_agent(
    selected_flight
):

    print("="*60)
    print("BOOKING AGENT")
    print("="*60)

    passenger = input(
        "\nPassenger name: "
    )

    return {

        "passenger_name":
        passenger,

        "flight":
        selected_flight,

        "booking_status":
        "CONFIRMED"
    }