from .state import (
    load_state
)


def booking_notification():

    state = load_state()

    selected = state.get(
        "selected_option",
        {}
    )

    customer = state.get(
        "customer_details",
        {}
    )


    return f"""

BOOKING CONFIRMED

Customer:
{customer.get("name")}

Phone:
{customer.get("phone")}

Flight:
{selected.get("flight_type")}

Price:
{selected.get("price")}

Payment:
{state.get("payment_status")}

"""