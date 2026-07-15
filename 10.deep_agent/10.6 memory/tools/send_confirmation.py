# ============================================================
# TOOL: SEND CONFIRMATION
# ============================================================

from langchain_core.tools import tool
from .state import conversation_state
from .notification_agent import notification_agent


@tool
def send_confirmation() -> str:
    """
    Generate booking confirmation details using notification agent.
    """
    if conversation_state["booking_details"] is None:
        return "Booking incomplete."

    # Delegate confirmation generation to the notification agent passing computed context
    return notification_agent({
        "booking_status": conversation_state["booking_details"]["booking_status"],
        "flight": conversation_state["current_flight"]
    })
