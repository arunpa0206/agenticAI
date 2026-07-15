# ====================================================
# TOOL: CONFIRM TICKET
# ====================================================

from langchain.tools import tool
from .state import load_state, save_state
from .filesys import FileService


@tool
def confirm_ticket(
    customer_name: str,
    phone: str,
    payment_confirmed: bool
):
    """
    Confirms the ticket booking once payment is confirmed,
    saves the details to state, and exports external filesystem records.
    """
    state = load_state()

    # Pre-condition: payment must be confirmed to book the ticket
    if not payment_confirmed:
        return "Payment failed"

    # Populate customer information and update payment status
    state["customer"] = {
        "name": customer_name,
        "phone": phone
    }
    state["payment_status"] = "PAID"
    
    # Save the updated workflow state
    save_state(state)

    # Invoke filesystem service to create external records (txt, json, csv)
    FileService.create_external_records(state)
    
    return "Booking confirmed and files created"
