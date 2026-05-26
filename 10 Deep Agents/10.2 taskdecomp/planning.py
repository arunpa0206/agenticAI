from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic

from search import search_flights
from passenger_details import enter_passenger_details
from seat_selection import select_seat
from payment_confirmation import payment_confirmation


# ====================================================
# MODEL
# ====================================================

model = ChatAnthropic(

    model="claude-sonnet-4-20250514",

    api_key="YOUR_API_KEY"
)


# ====================================================
# CREATE DEEP AGENT
# ====================================================

agent = create_deep_agent(

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

def run_agent():

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

        print(
            final_message.content
        )


        # Store assistant response
        conversation.append(

            {

                "role":"assistant",

                "content":
                final_message.content

            }

        )