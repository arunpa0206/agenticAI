# notification_worker.py

from langchain.tools import tool


@tool
def notification_worker(
    booking_details: str
):
    """
    Generate a booking confirmation
    message after successful payment.
    """

    return f"""

BOOKING CONFIRMED

Details:

{booking_details}

Payment Successful

Have a safe journey.

"""