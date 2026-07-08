from deepagents import create_deep_agent
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

from search_tool import search_tool
from payment_tool import payment_tool
from notification_tool import notification_tool

import uuid


# ============================================================
# CLAUDE API
# ============================================================

llm = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-5"
)


# ============================================================
# SHARED STATE
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
    Search one flight only
    """

    conversation_state[
        "source"
    ] = source

    conversation_state[
        "destination"
    ] = destination


    flight = search_tool(

        {

            "source":
            source,

            "destination":
            destination

        }

    )


    conversation_state[
        "current_flight"
    ] = flight


    return (

        f"\nFlight Found\n"
        f"-------------------------\n"

        f"Flight ID : {flight['flight_id']}\n"

        f"Airline   : {flight['airline']}\n"

        f"Route     : {flight['source']} → "
        f"{flight['destination']}\n"

        f"Departure : {flight['time']}\n"

        f"Price     : {flight['price']}\n"

        f"\nType:\n"

        f"- yes\n"
        f"- another"

    )


# ============================================================
# ANOTHER FLIGHT TOOL
# ============================================================

@tool
def another_flight()->str:

    """
    Generate another flight
    """

    travel_plan = {

        "source":

        conversation_state[
            "source"
        ],

        "destination":

        conversation_state[
            "destination"
        ]

    }


    flight = search_tool(
        travel_plan
    )


    conversation_state[
        "current_flight"
    ] = flight


    return (

        f"\nNew Flight Found\n"
        f"-------------------------\n"

        f"Flight ID : {flight['flight_id']}\n"

        f"Airline   : {flight['airline']}\n"

        f"Route     : {flight['source']} → "
        f"{flight['destination']}\n"

        f"Departure : {flight['time']}\n"

        f"Price     : {flight['price']}\n"

        f"\nType:\n"

        f"- yes\n"
        f"- another"

    )


# ============================================================
# PAYMENT TOOL
# ============================================================

@tool
def make_payment()->str:

    """
    Complete payment
    """

    booking = payment_tool(

        conversation_state[
            "current_flight"
        ]

    )


    conversation_state[
        "booking_details"
    ] = booking


    return (
        "Payment completed."
    )


# ============================================================
# CONFIRMATION TOOL
# ============================================================

@tool
def send_confirmation()->str:

    """
    Generate confirmation
    """

    return notification_tool(

        conversation_state[
            "booking_details"
        ]

    )


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """

You are a flight booking assistant.

Rules:

- Show only ONE flight at a time
- Never show multiple flights

If user says:

another
next
different

call another_flight()

Replace old flight completely

If user says:

yes
book
proceed

call make_payment()

After payment:

call send_confirmation()

Never invent flights

Use tool output only

"""


# ============================================================
# CREATE AGENT
# ============================================================

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
    MemorySaver()

)


# ============================================================
# SESSION CONFIG
# ============================================================

config = {

    "configurable":{

        "thread_id":
        str(uuid.uuid4())

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

            # Send message to agent
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