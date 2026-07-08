import warnings
warnings.filterwarnings("ignore")

from langchain.tools import tool
from deepagents import create_deep_agent
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic

from search_worker import search_worker
from booking_worker import booking_worker
from notification_worker import notification_worker


# ============================================================
# PLANNING TOOL
# ============================================================

@tool
def planning_agent(
    user_query: str
):

    """
    Extract travel information.
    """

    text = user_query.lower()

    source = "Bangalore"
    destination = "Delhi"

    words = text.split()


    # Extract source city
    if "from" in words:

        idx = words.index(
            "from"
        )

        if idx + 1 < len(words):

            source = words[
                idx + 1
            ]


    # Extract destination city
    if "to" in words:

        idx = words.index(
            "to"
        )

        if idx + 1 < len(words):

            destination = words[
                idx + 1
            ]


    return {

        "source":
        source.title(),

        "destination":
        destination.title()

    }


# ============================================================
# MODEL
# ============================================================

model = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model=
    "claude-sonnet-5"
)


# ============================================================
# CREATE DEEP AGENT
# ============================================================

agent = create_deep_agent(

    model=model,

    tools=[

        planning_agent,

        search_worker,

        booking_worker,

        notification_worker

    ],

    system_prompt="""

You are a Flight Booking Agent.

Rules:

If source and destination
are required:

use planning_agent()

If flight search is needed:

use search_worker()

If user wants booking:

use booking_worker()

After booking:

use notification_worker()

Continue previous workflow.

Avoid restarting.

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


        # Store user message
        conversation.append(

            {

                "role":
                "user",

                "content":
                query
            }

        )


        # Send messages to agent
        response = agent.invoke({

            "messages":
            conversation

        })


        final = response[
            "messages"
        ][-1]


        print(
            "\nAgent:\n"
        )

        print(
            final.content
        )


        # Store agent response
        conversation.append(

            {

                "role":
                "assistant",

                "content":
                final.content
            }

        )