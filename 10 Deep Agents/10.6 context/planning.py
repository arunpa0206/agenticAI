from deepagents import create_deep_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

from search_agent import search_agent
from payment_agent import payment_agent
from notification_agent import notification_agent

import uuid


# ============================================================
# CLAUDE API
# ============================================================

llm = ChatAnthropic(

    model=
    "claude-sonnet-4-20250514",

    api_key="YOUR_API_KEY"
)


# ============================================================
# CONVERSATION STATE
# ============================================================

conversation_state = {

    "source":None,

    "destination":None,

    "current_flight":None,

    "booking_details":None

}


# ============================================================
# SEARCH TOOL
# ============================================================

@tool
def search_flight(
    source:str,
    destination:str
)->str:

    """
    Search for flight
    """

    conversation_state[
        "source"
    ]=source

    conversation_state[
        "destination"
    ]=destination


    flight = search_agent(

        {

            "source":
            source,

            "destination":
            destination

        }

    )


    conversation_state[
        "current_flight"
    ]=flight


    return (

        f"\nFlight Found\n"
        f"-------------------------\n"

        f"Flight ID : {flight['flight_id']}\n"

        f"Airline   : {flight['airline']}\n"

        f"Route     : {flight['source']} → "
        f"{flight['destination']}\n"

        f"Departure : {flight['time']}\n"

        f"Price     : {flight['price']}\n"

        f"\nSay 'yes' to book "
        f"or 'another' for a different flight."

    )


# ============================================================
# ANOTHER FLIGHT TOOL
# ============================================================

@tool
def another_flight()->str:

    """
    Generate another flight
    """

    source = conversation_state[
        "source"
    ]

    destination = conversation_state[
        "destination"
    ]


    if source is None:

        return (
            "No route available yet."
        )


    flight = search_agent(

        {

            "source":
            source,

            "destination":
            destination

        }

    )


    conversation_state[
        "current_flight"
    ]=flight


    return (

        f"\nNew Flight Found\n"
        f"-------------------------\n"

        f"Flight ID : {flight['flight_id']}\n"

        f"Airline   : {flight['airline']}\n"

        f"Route     : {flight['source']} → "
        f"{flight['destination']}\n"

        f"Departure : {flight['time']}\n"

        f"Price     : {flight['price']}\n"

        f"\nSay 'yes' to book "
        f"or 'another' for another flight."

    )


# ============================================================
# PAYMENT TOOL
# ============================================================

@tool
def make_payment()->str:

    """
    Complete payment
    """

    flight = conversation_state[
        "current_flight"
    ]


    if flight is None:

        return (
            "No flight selected."
        )


    booking = payment_agent(

        {

            "flight_id":
            flight["flight_id"],

            "price":
            flight["price"],

            "airline":
            flight["airline"]

        }

    )


    conversation_state[
        "booking_details"
    ]=booking


    return (
        "Payment completed successfully."
    )


# ============================================================
# CONFIRMATION TOOL
# ============================================================

@tool
def send_confirmation()->str:

    """
    Generate confirmation
    """

    if (

        conversation_state[
            "booking_details"
        ] is None

    ):

        return (
            "Booking incomplete."
        )


    return notification_agent(

        {

            "booking_status":

            conversation_state[
                "booking_details"
            ][
                "booking_status"
            ],

            "flight":

            conversation_state[
                "current_flight"
            ]

        }

    )


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """

You are a flight booking assistant.

Rules:

- Show ONE flight at a time
- Never list multiple flights

If user says:

another
next
different
change flight
new flight

call another_flight()

Replace old flight completely

If user says:

yes
proceed
book

call make_payment()

After payment:

call send_confirmation()

Never invent flights

Use only tool results

"""


# ============================================================
# AGENT
# ============================================================

memory = MemorySaver()

agent = create_deep_agent(

    model=llm,

    tools=[

        search_flight,

        another_flight,

        make_payment,

        send_confirmation

    ],

    system_prompt=
    SYSTEM_PROMPT,

    checkpointer=
    memory
)


# ============================================================
# SESSION CONFIG
# ============================================================

config = {

    "configurable":{

        "thread_id":

        f"session-{uuid.uuid4()}"

    }

}


# ============================================================
# AGENT FUNCTION
# ============================================================

def run_agent():

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


        try:

            # Send query to agent
            result = agent.invoke(

                {

                    "messages":[

                        {

                            "role":"user",

                            "content":
                            query

                        }

                    ]

                },

                config=config

            )


            print(
                "\nAssistant:"
            )


            print(

                result[
                    "messages"
                ][-1]
                .content

            )


        except Exception as e:

            print(

                "\nError:",
                str(e)

            )