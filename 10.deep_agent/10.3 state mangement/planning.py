from deepagents import create_deep_agent
import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic

from tools.tools import (
    generate_flight_plan,
    booking_workflow,
    payment_workflow,
    notification_workflow
)


# ==================================================
# MODEL
# ==================================================

def create_model():
    return ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-sonnet-5"
    )


# ==================================================
# DEEP AGENT
# ==================================================

def create_agent(model):
    return create_deep_agent(
        model=model,
        tools=[
            generate_flight_plan,
            booking_workflow,
            payment_workflow,
            notification_workflow
        ],
        system_prompt="""

You are a Flight Deep Agent.

Rules:

1. If user asks for flight:

   call:

   generate_flight_plan()

2. If user says:

   "another flight"
   "show another"
   "next flight"
   "different flight"
   "generate another flight"

   call:

   generate_flight_plan()

   and replace previous flight

3. If user says:

   "book another flight"
   "book different flight"
   "change booking"

   generate new flight
   and restart booking flow

4. If user wants booking:

   collect:

   customer_name
   phone

   then call:

   booking_workflow(
      customer_name,
      phone
   )

5. Ask for payment
   confirmation

6. If payment confirmed:

   payment_workflow(
      payment_confirmed=True
   )

7. After payment:

   notification_workflow()

8. Continue workflow
   using previous state

"""
    )


# ==================================================
# AGENT FUNCTION
# ==================================================

def run_agent(agent=None):
    if agent is None:
        model = create_model()
        agent = create_agent(model)

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

        # Send conversation to agent
        response = agent.invoke(
            {
                "messages":
                conversation
            }
        )

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

        # Store assistant reply
        conversation.append(
            {
                "role":
                "assistant",
                "content":
                final_message.content
            }
        )


def main():
    model = create_model()
    agent = create_agent(model)
    run_agent(agent)


if __name__ == "__main__":
    main()