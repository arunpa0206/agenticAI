import random
import requests

from langchain.tools import tool
from deepagents import create_deep_agent
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic


# ============================================================
# BOOKING API
# ============================================================

BOOKING_API_URL = (
    "https://jsonplaceholder.typicode.com/posts"
)


# ============================================================
# FLIGHT OPTIONS
# ============================================================

flight_options = [

    {
        "flight_type": "Economy",
        "travel_time": "2.5 Hours",
        "price": "₹5,200"
    },

    {
        "flight_type": "Business",
        "travel_time": "2 Hours",
        "price": "₹11,500"
    },

    {
        "flight_type": "Premium Economy",
        "travel_time": "2 Hours 20 Minutes",
        "price": "₹7,800"
    },

    {
        "flight_type": "Budget Saver",
        "travel_time": "3 Hours",
        "price": "₹4,100"
    }

]


# ============================================================
# PREVENT SAME FLIGHT TWICE
# ============================================================

previous_flight = None


# ============================================================
# TOOL → GENERATE FLIGHT
# ============================================================

@tool
def generate_flight_option():

    """
    Generate flight option
    without immediate repeats.
    """

    global previous_flight

    available = [

        flight

        for flight in flight_options

        if flight != previous_flight
    ]

    selected = random.choice(
        available
    )

    previous_flight = selected

    return f"""

Flight Details

Flight Type:
{selected["flight_type"]}

Travel Time:
{selected["travel_time"]}

Price:
{selected["price"]}

Would you like to proceed with
this booking or would you like
another flight option?

"""


# ============================================================
# TOOL → BOOKING API
# ============================================================

@tool
def create_booking(
    from_city: str,
    to_city: str
):

    """
    Create booking.
    """

    payload = {

        "from":
        from_city,

        "to":
        to_city
    }

    response = requests.post(

        BOOKING_API_URL,
        json=payload
    )

    return response.json()


# ============================================================
# TOOL → FINAL BOOKING
# ============================================================

@tool
def booking_agent(
    from_city: str,
    to_city: str,
    flight_type: str
):

    """
    Complete booking.
    """

    booking = create_booking.invoke({

        "from_city":
        from_city,

        "to_city":
        to_city
    })

    return f"""

BOOKING CONFIRMED

Route:
{from_city} → {to_city}

Flight Type:
{flight_type}

Booking ID:
{booking.get("id")}

Status:
Confirmed

"""


# ============================================================
# MODEL
# ============================================================

model = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-5"
)


# ============================================================
# CREATE DEEP AGENT
# ============================================================

agent = create_deep_agent(

    model=model,

    tools=[

        generate_flight_option,
        create_booking,
        booking_agent
    ],

    system_prompt="""

You are a Flight Deep Agent.

Responsibilities:

- Understand travel intent
- Generate flight options
- Preserve context across turns
- Continue workflows naturally
- Use tools only when needed
- Continue existing workflows

Do not show numbered menus.

Do not restart workflows.

Do not invent flight information.

Use previous conversation context.

If user asks:

"show another option"

call generate_flight_option()

If user asks:

"proceed"
"book"
"confirm"

continue booking flow.

"""
)


# ============================================================
# AGENT LOOP FUNCTION
# ============================================================

def run_agent():

    conversation = []

    while True:

        user_query = input(
            "\nYou: "
        )


        if user_query.lower() in [

            "exit",
            "quit"

        ]:

            print(
                "\nGoodbye!"
            )

            break


        conversation.append(

            {

                "role":
                "user",

                "content":
                user_query

            }

        )


        response = agent.invoke({

            "messages":
            conversation

        })


        final_message = (

            response[
                "messages"
            ][-1]
        )


        print(
            "\nAgent:\n"
        )

        print(
            final_message.content
        )


        conversation.append(

            {

                "role":
                "assistant",

                "content":
                final_message.content

            }

        )