def send_confirmation(
    user_name,
    flight_number
):

    return f"""
=========================================
         BOOKING CONFIRMED
=========================================

Passenger Name : {user_name}
Flight Number  : {flight_number}
Status          : Confirmed

Your ticket has been booked successfully.

Thank you for choosing our service.
Have a safe journey.

=========================================
"""