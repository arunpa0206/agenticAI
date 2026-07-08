import json
import os


STATE_FOLDER = "workflow_state"

STATE_FILE = (
    f"{STATE_FOLDER}/state.json"
)


if not os.path.exists(
    STATE_FOLDER
):
    os.makedirs(
        STATE_FOLDER
    )


DEFAULT_STATE = {

    "current_step": None,

    "selected_option": {},

    "customer_details": {},

    "payment_status": "NOT_PAID",

    "booking_status": "NOT_BOOKED"
}


def save_state(
    state
):

    with open(

        STATE_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            state,

            file,

            indent=4,

            ensure_ascii=False

        )


def load_state():

    if not os.path.exists(
        STATE_FILE
    ):

        save_state(
            DEFAULT_STATE
        )

        return DEFAULT_STATE.copy()


    with open(

        STATE_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        state = json.load(
            file
        )


    for key, value in DEFAULT_STATE.items():

        if key not in state:

            state[key] = value


    return state