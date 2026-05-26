from deepagents import create_deep_agent
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

from premium_business import premium_business_search
from cheapest_flight import cheapest_flight_search
from nonstop_reasonable import nonstop_reasonable_search

from payment_tasks import (
    validate_payment,
    process_transaction,
    update_payment_status
)

from notification_tasks import (
    generate_ticket,
    send_confirmation_email,
    update_booking_record,
    notification_results
)

import threading
import uuid


# ============================================================
# CLAUDE MODEL
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

    "flights":[],
    "selected_flight":None

}


# ============================================================
# SEARCH FLIGHTS TOOL
# ============================================================

@tool
def search_flights(
    source:str,
    destination:str
)->str:

    """
    Run parallel flight search
    """

    results=[]


    # Start parallel search threads
    t1 = threading.Thread(

        target=
        premium_business_search,

        args=(results,)

    )

    t2 = threading.Thread(

        target=
        cheapest_flight_search,

        args=(results,)

    )

    t3 = threading.Thread(

        target=
        nonstop_reasonable_search,

        args=(results,)

    )


    t1.start()
    t2.start()
    t3.start()


    t1.join()
    t2.join()
    t3.join()


    conversation_state[
        "flights"
    ] = results


    output = "\nAvailable Flights\n\n"


    for i,flight in enumerate(

        results,
        start=1

    ):

        output += (

            f"{i}. "

            f"{flight['flight_type']} | "

            f"{flight['airline']} | "

            f"{flight['flight']} | "

            f"{flight['price']}\n"

        )


    output += (

        "\nSelect 1,2 or 3"

    )


    return output


# ============================================================
# SELECT FLIGHT TOOL
# ============================================================

@tool
def select_flight(
    choice:int
)->str:

    """
    Select a flight
    """

    selected = conversation_state[
        "flights"
    ][choice-1]


    conversation_state[
        "selected_flight"
    ] = selected


    return (

        f"Selected:\n"

        f"{selected['airline']} "

        f"{selected['flight']}"

    )


# ============================================================
# BOOK FLIGHT TOOL
# ============================================================

@tool
def book_flight()->str:

    """
    Complete booking
    """


    # Payment threads
    p1 = threading.Thread(
        target=validate_payment
    )

    p2 = threading.Thread(
        target=process_transaction
    )

    p3 = threading.Thread(
        target=update_payment_status
    )


    p1.start()
    p2.start()
    p3.start()


    p1.join()
    p2.join()
    p3.join()


    # Notification threads
    n1 = threading.Thread(

        target=
        generate_ticket,

        args=(

            conversation_state[
                "selected_flight"
            ],

        )

    )


    n2 = threading.Thread(
        target=send_confirmation_email
    )

    n3 = threading.Thread(
        target=update_booking_record
    )


    n1.start()
    n2.start()
    n3.start()


    n1.join()
    n2.join()
    n3.join()


    return notification_results[
        "ticket"
    ]


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """

Rules:

Search
=
call search_flights()

If user says:

1
2
3

call select_flight()

If user says:

yes
book
proceed

call book_flight()

"""


# ============================================================
# CREATE AGENT
# ============================================================

agent = create_deep_agent(

    model=llm,

    tools=[

        search_flights,
        select_flight,
        book_flight

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