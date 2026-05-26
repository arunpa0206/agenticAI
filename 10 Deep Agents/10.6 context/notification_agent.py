# notification_agent.py
# Notification Agent


def notification_agent(
    notification_context
):

    print("\n" + "=" * 60)
    print("NOTIFICATION AGENT")
    print("=" * 60)

    print(
        "\nUsing notification context:\n"
    )

    print(notification_context)

    flight = notification_context["flight"]

    confirmation = f"""
BOOKING CONFIRMED

Status      : {notification_context["booking_status"]}
Flight ID   : {flight["flight_id"]}
Airline     : {flight["airline"]}
Source      : {flight["source"]}
Destination : {flight["destination"]}
Time         : {flight["time"]}
Price        : {flight["price"]}

Thank you for booking with us.
"""

    return confirmation