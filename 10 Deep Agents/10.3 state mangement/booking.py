from state import (
    load_state,
    save_state
)


def save_booking(
    customer_name:str,
    phone:str
):

    state = load_state()

    state["customer_details"] = {

        "name":
        customer_name,

        "phone":
        phone
    }

    state[
        "current_step"
    ] = "CUSTOMER_DETAILS_COMPLETED"


    save_state(
        state
    )


    return f"""

Customer details saved

Name:
{customer_name}

Phone:
{phone}

"""