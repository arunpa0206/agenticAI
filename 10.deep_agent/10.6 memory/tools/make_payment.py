# ============================================================
# TOOL: MAKE PAYMENT
# ============================================================

from langchain_core.tools import tool
from .state import conversation_state
from .payment_agent import payment_agent


@tool
def make_payment() -> str:
    """
    Initiate and complete payment process for the selected flight.
    """
    flight = conversation_state["current_flight"]
    if flight is None:
        return "No flight selected."

    # Call payment agent passing current flight context details
    booking = payment_agent({
        "flight_id": flight["flight_id"],
        "price": flight["price"],
        "airline": flight["airline"]
    })
    conversation_state["booking_details"] = booking

    return "Payment completed successfully."
