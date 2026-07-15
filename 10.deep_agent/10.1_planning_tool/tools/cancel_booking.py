import random
from langchain.tools import tool

@tool
def cancel_booking(booking_id: str):
    """
    Cancels an existing booking using its unique Booking ID.
    Returns a cancellation confirmation status.
    """
    return {
        "booking_id": booking_id,
        "status": "Cancelled"
    }
