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

from tools.payment import payment_workflow
from tools.notification import notification_workflow
from tools.human_operator import wait_for_approval, get_approved_flights

from tools.premium_business import premium_business_search
from tools.cheapest_flight import cheapest_flight_search
from tools.nonstop_reasonable import nonstop_reasonable_search


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

    wait_for_approval()
    approved = get_approved_flights()


    if len(
        approved
    ) == 0:

        return """

We are sorry.

No flights are currently
available.

Please try again later.

"""


    output = "\n### Approved Flight Options:\n\n"
    output += "| Option | Flight ID | Airline | Type | Price |\n"
    output += "|---|---|---|---|---|\n"
    for idx, flight in enumerate(approved):
        output += f"| {idx + 1} | {flight['flight_id']} | {flight['airline']} | {flight['type']} | {flight['price']} |\n"

    output += "\nWhich flight option do you want to proceed with? (Enter the option number or Flight ID)\n"
    return output


# ============================================================
# BOOKING TOOL
# ============================================================

@tool
def process_booking(selection: str = ""):
    """
    Process booking by choosing the selected flight (by option number or flight ID).
    """
    approved = get_approved_flights()

    if len(approved) == 0:
        return "No approved flights found to book."

    selected = None
    choice = selection.strip()

    # Try to resolve choice from passed parameter first
    if choice:
        try:
            val = int(choice) - 1
            if 0 <= val < len(approved):
                selected = approved[val]
        except ValueError:
            for flight in approved:
                if flight['flight_id'].lower() == choice.lower():
                    selected = flight
                    break

        if not selected:
            print(f"\nInvalid selection: '{selection}'")

    # Fallback to console prompt only if choice was invalid/missing
    if not selected:
        print("\nApproved flights:")
        for idx, flight in enumerate(approved):
            print(f"[{idx + 1}] {flight['flight_id']} - {flight['airline']} ({flight['type']}) at {flight['price']}")

        while not selected:
            choice = input("\nWhich flight do you want to proceed with? (Enter number or Flight ID): ").strip()
            try:
                val = int(choice) - 1
                if 0 <= val < len(approved):
                    selected = approved[val]
                else:
                    print("Invalid number. Please choose from the list.")
            except ValueError:
                # Check by flight ID
                for flight in approved:
                    if flight['flight_id'].lower() == choice.lower():
                        selected = flight
                        break
                if not selected:
                    print("Invalid input. Please enter the number or Flight ID.")

    payment = payment_workflow(selected)
    notification_workflow(selected, payment)

    return f"Booking completed for flight {selected['flight_id']}"


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

5. If approved flights exist, display them in the markdown table returned by the tool and ask:

"Which flight option do you want to proceed with?"

6. When the user specifies an option (e.g., Option number or Flight ID or selection details), call:

process_booking(selection=<user selection>)

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

def start_agent():

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

        content = msg.content
        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                elif hasattr(block, "type") and getattr(block, "type") == "text":
                    text_parts.append(getattr(block, "text", ""))
                elif isinstance(block, str):
                    text_parts.append(block)
            output_text = "".join(text_parts)
        else:
            output_text = str(content)

        print(output_text)


        # Store assistant reply
        conversation.append(

            {

                "role":
                "assistant",

                "content":
                msg.content

            }

        )