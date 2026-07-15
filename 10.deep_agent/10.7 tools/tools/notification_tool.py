# notification_tool.py

def notification_tool(
    booking_details
):

    flight = booking_details[
        "flight"
    ]

    return f"""

BOOKING CONFIRMED

Status      : {booking_details['booking_status']}
Flight ID   : {flight['flight_id']}
Airline     : {flight['airline']}
Route       : {flight['source']} → {flight['destination']}
Time        : {flight['time']}
Price       : {flight['price']}

Thank you for booking with us.
"""