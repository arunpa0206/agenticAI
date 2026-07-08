import json
import time

from deepagents import create_deep_agent
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic

from payment import payment_workflow
from notification import notification_workflow
from human_operator import wait_for_approval

from premium_business import premium_business_search
from cheapest_flight import cheapest_flight_search
from nonstop_reasonable import nonstop_reasonable_search


# ============================================================
# FILE STORAGE
# ============================================================

FLIGHT_FILE = (
    "flight_options.json"
)


# ============================================================
# GENERATE FLIGHTS TOOL
# ============================================================

@tool
def generate_flights():

    """
    Generate flights
    """

    flights = []


    # Generate premium flights
    for _ in range(5):

        flights.append(
            premium_business_search()
        )


    # Generate cheapest flights
    for _ in range(5):

        flights.append(
            cheapest_flight_search()
        )


    # Generate nonstop flights
    for _ in range(5):

        flights.append(
            nonstop_reasonable_search()
        )


    # Add IDs and status
    for i, flight in enumerate(

        flights,
        start=1

    ):

        flight[
            "flight_number"
        ] = i


        flight[
            "approval_status"
        ] = "NOT_APPROVED"


    # Save flight data
    with open(

        FLIGHT_FILE,
        "w",
        encoding="utf-8"

    ) as file:

        json.dump(

            flights,
            file,
            indent=4

        )


    return """

Searching for flights...

Flight options generated.

Our flight operator
is reviewing flights.

"""


# ============================================================
# APPROVAL TOOL
# ============================================================

@tool
def approval_checkpoint():

    """
    Human approval step
    """

    approved = wait_for_approval()


    if len(
        approved
    ) == 0:

        return """

We are sorry.

No flights are currently
available.

Please try again later.

"""


    output = (

        "\nAPPROVED FLIGHTS\n"

    )


    for flight in approved:

        output += f"""

Flight ID:
{flight["flight_id"]}

Airline:
{flight["airline"]}

Type:
{flight["type"]}

Price:
{flight["price"]}

"""


    output += """

Do you want
to proceed?

"""

    return output


# ============================================================
# BOOKING TOOL
# ============================================================

@tool
def process_booking():

    """
    Process booking
    """

    approved = wait_for_approval()

    selected = approved[0]


    payment = (

        payment_workflow(
            selected
        )

    )


    notification_workflow(

        selected,
        payment

    )


    return (
        "Booking completed"
    )


# ============================================================
# MODEL
# ============================================================

model = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model=
    "claude-sonnet-5"
)


# ============================================================
# CREATE AGENT
# ============================================================

agent = create_deep_agent(

    model=model,

    tools=[

        generate_flights,
        approval_checkpoint,
        process_booking

    ],

    system_prompt="""

You are a Human-in-the-Loop
Flight Assistant.

Rules:

1. Never invent flights.

2. Flights only come from:

generate_flights()

3. If user says:

find flight
show flight

call:

generate_flights()

4. After generating:

call:

approval_checkpoint()

5. If approved flights exist:

ask:

Do you want to proceed?

6. If user says:

proceed
book
confirm
continue
yes

call:

process_booking()

7. If user says:

another flight
different flight
show more
next flight

DO NOT call
generate_flights()

Immediately reply:

We are sorry.

No flights are currently
available.

Please try again later.

8. Never bypass tools

"""

)


# ============================================================
# AGENT FUNCTION
# ============================================================

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

                "role":
                "user",

                "content":
                query

            }

        )


        # Send query to agent
        result = agent.invoke(

            {

                "messages":
                conversation

            }

        )


        msg = (

            result[
                "messages"
            ][-1]

        )


        print(
            "\nAgent:\n"
        )

        print(
            msg.content
        )


        # Store assistant reply
        conversation.append(

            {

                "role":
                "assistant",

                "content":
                msg.content

            }

        )