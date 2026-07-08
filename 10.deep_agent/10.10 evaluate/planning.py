from deepagents import create_deep_agent
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

from evaluation import (
    evaluate_workflow,
    display_metrics
)

import time
import random
import uuid


# ============================================================
# CLAUDE API
# ============================================================

llm = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model=
    "claude-sonnet-5"
)


# ============================================================
# SHARED STATE
# ============================================================

conversation_state = {

    "source":None,

    "destination":None,

    "current_flight":None,

    "payment_result":None,

    "start_time":None
}


# ============================================================
# SEARCH FLIGHT TOOL
# ============================================================

@tool
def search_flight(
    source:str,
    destination:str
)->str:

    """
    Generate one flight
    """

    conversation_state[
        "source"
    ] = source

    conversation_state[
        "destination"
    ] = destination

    conversation_state[
        "start_time"
    ] = time.time()


    flight = {

        "flight_id":
        f"FL{random.randint(100,999)}",

        "from":
        source,

        "to":
        destination,

        "time":
        random.choice(

            [

                "6:30 PM",
                "8:15 PM",
                "10:45 PM"

            ]

        ),

        "price":
        random.choice(

            [

                "₹4800",
                "₹5200",
                "₹6100"

            ]

        )

    }


    conversation_state[
        "current_flight"
    ] = flight


    return (

        f"\nFlight Found\n"

        f"----------------------\n"

        f"Flight : "
        f"{flight['flight_id']}\n"

        f"Route : "
        f"{flight['from']} → "
        f"{flight['to']}\n"

        f"Time : "
        f"{flight['time']}\n"

        f"Price : "
        f"{flight['price']}\n\n"

        f"Type:\n"

        f"- yes\n"
        f"- another"

    )


# ============================================================
# ANOTHER FLIGHT TOOL
# ============================================================

@tool
def another_flight()->str:

    """
    Replace current flight
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
# PAYMENT TOOL
# ============================================================

@tool
def process_payment()->str:

    """
    Process payment
    """

    flight = conversation_state[
        "current_flight"
    ]


    print(
        "\n[PAYMENT AGENT]"
    )


    time.sleep(2)


    if random.random() < 0.2:

        payment_result = {

            "status":
            "FAILED"

        }

    else:

        payment_result = {

            "status":
            "SUCCESS"

        }


    conversation_state[
        "payment_result"
    ] = payment_result


    confirmation = (

        f"\nBOOKING RESULT\n"

        f"----------------------\n"

        f"Flight : "
        f"{flight['flight_id']}\n"

        f"Status : "
        f"{payment_result['status']}\n"

    )


    total_time = (

        time.time()

        -

        conversation_state[
            "start_time"
        ]

    )


    metrics = evaluate_workflow(

        payment_result=
        payment_result,

        total_time=
        total_time,

        user_query=
        f"{flight['from']} to {flight['to']}",

        assistant_output=
        confirmation,

        tool_calls=3,

        failed_tools=0,

        retries=0

    )


    display_metrics(
        metrics
    )


    return confirmation


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """

Rules:

Show only ONE flight

another
next
change

= different flight

yes
book
proceed

= process_payment

Replace old flight completely

Never show history

"""


# ============================================================
# CREATE AGENT
# ============================================================

agent = create_deep_agent(

    model=llm,

    tools=[

        search_flight,
        another_flight,
        process_payment

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

                        "role":"user",

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