from state import (
    load_state,
    save_state
)


def process_payment(
    payment_confirmed:bool
):

    state = load_state()


    if not payment_confirmed:

        return (
            "Payment failed"
        )


    state[
        "payment_status"
    ] = "PAID"


    state[
        "booking_status"
    ] = "BOOKED"


    state[
        "current_step"
    ] = "PAYMENT_COMPLETED"


    save_state(
        state
    )


    return (
        "Payment successful"
    )