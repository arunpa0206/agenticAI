from langchain.tools import tool
import random

from state import (
    load_state,
    save_state
)

from booking import (
    save_booking
)

from payment import (
    process_payment
)

from notification import (
    booking_notification
)


flight_options = [

    {
        "flight_type": "Economy",
        "travel_time": "2.5 Hours",
        "price": "₹5200"
    },

    {
        "flight_type": "Business",
        "travel_time": "2 Hours",
        "price": "₹11500"
    },

    {
        "flight_type": "Premium Economy",
        "travel_time": "2 Hours 20 Minutes",
        "price": "₹7800"
    },

    {
        "flight_type": "Budget Saver",
        "travel_time": "3 Hours",
        "price": "₹4100"
    }

]


@tool
def generate_flight_plan():

    """
    Generate a flight plan
    or regenerate another flight.
    """

    selected = random.choice(
        flight_options
    )

    state = load_state()

    state["selected_option"] = (
        selected
    )

    state["customer_details"] = {}

    state["payment_status"] = (
        "NOT_PAID"
    )

    state["booking_status"] = (
        "NOT_BOOKED"
    )

    state["current_step"] = (
        "FLIGHT_GENERATED"
    )

    save_state(
        state
    )

    return selected


@tool
def booking_workflow(
    customer_name: str,
    phone: str
):

    """
    Save customer booking details.
    """

    return save_booking(

        customer_name,
        phone
    )


@tool
def payment_workflow(
    payment_confirmed: bool
):

    """
    Process customer payment.
    """

    return process_payment(

        payment_confirmed
    )


@tool
def notification_workflow():

    """
    Generate booking confirmation.
    """

    return booking_notification()