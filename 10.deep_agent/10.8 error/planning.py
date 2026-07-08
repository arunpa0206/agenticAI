from deepagents import create_deep_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

from booking_agent import booking_agent
from error_handler import handle_error
from notification_agent import (
    success_notification,
    failure_notification
)

import random
import time
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
# SHARED CONVERSATION STATE
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

    current_time = int(
        time.time()
    )


    try:

        # Simulate random system failure
        if current_time % 2 == 0:

            raise Exception(
                "Flight search system failure"
            )


    except Exception:

        retry = handle_error()


        if not retry:

            failure_notification()

            return (
                "Search unavailable."
            )


    airlines = [

        "Air India",
        "IndiGo",
        "SpiceJet",
        "Vistara"

    ]


    times = [

        "06:30 AM",
        "09:15 AM",
        "12:45 PM",
        "04:20 PM"

    ]


    prices = [

        "₹5200",
        "₹6100",
        "₹7300",
        "₹8500"

    ]


    flight = {

        "flight_id":
        f"FL{random.randint(100,999)}",

        "airline":
        random.choice(
            airlines
        ),

        "time":
        random.choice(
            times
        ),

        "price":
        random.choice(
            prices
        ),

        "source":
        source,

        "destination":
        destination

    }


    conversation_state[
        "source"
    ] = source


    conversation_state[
        "destination"
    ] = destination


    conversation_state[
        "current_flight"
    ] = flight


    return (

        f"\nFlight Found\n"
        f"------------------\n"

        f"Flight ID : {flight['flight_id']}\n"

        f"Airline   : {flight['airline']}\n"

        f"Route     : {source} → {destination}\n"

        f"Time      : {flight['time']}\n"

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

    return search_flight.invoke(

        {

            "source":

            conversation_state[
                "source"
            ],

            "destination":

            conversation_state[
                "destination"
            ]

        }

    )


# ============================================================
# BOOK FLIGHT TOOL
# ============================================================

@tool
def book_flight()->str:

    """
    Book selected flight
    """

    booking = booking_agent(

        conversation_state[
            "current_flight"
        ]

    )


    conversation_state[
        "booking_details"
    ] = booking


    return success_notification(
        booking
    )


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """

You are a flight booking assistant.

Rules:

- Show ONE flight only
- Never show multiple flights

another
next
change

→ another_flight()

yes
book
proceed

→ book_flight()

Replace previous flight entirely

Never reuse previous flights

"""


# ============================================================
# CREATE AGENT
# ============================================================

memory = MemorySaver()

agent = create_deep_agent(

    model=llm,

    tools=[

        search_flight,

        another_flight,

        book_flight

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
        str(
            uuid.uuid4()
        )

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


        result = agent.invoke(

            {

                "messages":[

                    {

                        "role":
                        "user",

                        "content":
                        query

                    }

                ]

            },

            config=config

        )


        print(
            "\nAssistant:\n"
        )


        print(

            result[
                "messages"
            ][-1]
            .content

        )