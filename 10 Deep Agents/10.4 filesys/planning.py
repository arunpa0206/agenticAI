import json
import os
import random

from langchain.tools import tool
from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic

from filesys import (
    FileService
)


# ====================================================
# STATE
# ====================================================

STATE_FOLDER = "workflow_state"

STATE_FILE = (
    f"{STATE_FOLDER}/state.json"
)

os.makedirs(
    STATE_FOLDER,
    exist_ok=True
)


DEFAULT_STATE = {

    "current_step":None,

    "travel_plan":{},

    "customer":{},

    "payment_status":"NOT_PAID"
}


# ====================================================
# SAVE STATE
# ====================================================

def save_state(state):

    with open(

        STATE_FILE,
        "w",
        encoding="utf-8"

    ) as file:

        json.dump(

            state,
            file,
            indent=4

        )


# ====================================================
# LOAD STATE
# ====================================================

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

        return json.load(
            file
        )


# ====================================================
# FLIGHT DATA
# ====================================================

flights = [

    {
        "flight_id":"AI101",
        "airline":"Air India",
        "time":"10:30 AM",
        "price":"₹5200"
    },

    {
        "flight_id":"6E202",
        "airline":"IndiGo",
        "time":"2:15 PM",
        "price":"₹4300"
    },

    {
        "flight_id":"UK303",
        "airline":"Vistara",
        "time":"8:00 PM",
        "price":"₹7200"
    }
]


previous = None


# ====================================================
# GENERATE PLAN TOOL
# ====================================================

@tool
def generate_plan():

    """
    Generate flight plan
    """

    global previous

    available = [

        x for x in flights
        if x != previous
    ]

    selected = random.choice(
        available
    )

    previous = selected

    state = load_state()

    state[
        "travel_plan"
    ] = {

        "source":
        "Bangalore",

        "destination":
        "Delhi",

        **selected
    }

    state[
        "current_step"
    ] = "PLAN_GENERATED"

    save_state(
        state
    )

    return selected


# ====================================================
# CONFIRM TICKET TOOL
# ====================================================

@tool
def confirm_ticket(

    customer_name:str,
    phone:str,
    payment_confirmed:bool

):

    """
    Confirm booking
    """

    state = load_state()


    if not payment_confirmed:

        return (
            "Payment failed"
        )


    state[
        "customer"
    ] = {

        "name":
        customer_name,

        "phone":
        phone
    }


    state[
        "payment_status"
    ] = "PAID"


    save_state(
        state
    )


    FileService.create_external_records(
        state
    )


    return (

        "Booking confirmed "
        "and files created"

    )


# ====================================================
# MODEL
# ====================================================

model = ChatAnthropic(

    model=
    "claude-sonnet-4-20250514",

    api_key="YOUR_API_KEY"
)


# ====================================================
# CREATE AGENT
# ====================================================

agent = create_deep_agent(

    model=model,

    tools=[

        generate_plan,
        confirm_ticket
    ],

    system_prompt="""

You are a Flight Assistant.

If user asks for flight:

call generate_plan()

If user says:

book
confirm
proceed

collect:

customer_name
phone

then call:

confirm_ticket()

"""
)


# ====================================================
# AGENT FUNCTION
# ====================================================

def run_agent():

    conversation = []

    while True:

        # Get user input
        query = input(
            "\nYou: "
        )


        # Exit application
        if query.lower() in [

            "exit",
            "quit"

        ]:

            print(
                "\nGoodbye!"
            )

            break


        # Store user query
        conversation.append(

            {

                "role":"user",
                "content":query

            }

        )


        # Send to agent
        response = agent.invoke(

            {

                "messages":
                conversation

            }

        )


        msg = response[
            "messages"
        ][-1]


        print(
            "\nAgent:\n"
        )


        print(
            msg.content
        )


        # Store agent response
        conversation.append(

            {

                "role":"assistant",

                "content":
                msg.content

            }

        )