from deepagents import create_deep_agent
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic

from tools.search import search_flights
from tools.passenger_details import enter_passenger_details
from tools.seat_selection import select_seat
from tools.payment_confirmation import payment_confirmation


# ====================================================
# MODEL
# ====================================================

def create_model():
    return ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-sonnet-5"
    )


# ====================================================
# CREATE DEEP AGENT
# ====================================================

def create_agent(model):
    return create_deep_agent(
        model=model,
        tools=[
            search_flights,
            enter_passenger_details,
            select_seat,
            payment_confirmation
        ],
        system_prompt="""

You are a flight booking assistant.

You have access to tools.

Choose tools only when needed.

Decide the order dynamically
based on:

- user requests
- conversation history
- current booking progress

Do not assume a fixed workflow.

If information is missing,
ask for it.

Continue from previous state
instead of restarting.

"""
    )


# ====================================================
# AGENT FUNCTION
# ====================================================

def run_agent(agent=None):
    if agent is None:
        model = create_model()
        agent = create_agent(model)

    conversation = []

    while True:
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
                "role":"user",
                "content":query
            }
        )

        # Send conversation to agent
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

        content = final_message.content
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

        # Store assistant response
        conversation.append(
            {
                "role":"assistant",
                "content":
                final_message.content
            }
        )


def start_agent():
    model = create_model()
    agent = create_agent(model)
    run_agent(agent)