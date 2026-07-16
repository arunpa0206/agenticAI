from deepagents import create_deep_agent
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

from tools.booking_agent import booking_agent
from tools.error_handler import handle_error
from tools.notification_agent import (
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
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model=
    "claude-sonnet-5"
)


from tools.state import conversation_state
from tools.search_flight import search_flight


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

def start_agent():

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


        content = result["messages"][-1].content
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