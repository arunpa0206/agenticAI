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

from tools.search_worker import search_worker
from tools.booking_worker import booking_worker
from tools.notification_worker import notification_worker


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
    from_idx = -1
    if "from" in words:
        from_idx = words.index("from")
        if from_idx + 1 < len(words):
            source = words[from_idx + 1]

    # Extract destination city
    if "to" in words:
        start_search = from_idx if from_idx != -1 else 0
        try:
            idx = words.index("to", start_search)
        except ValueError:
            idx = words.index("to")
        if idx + 1 < len(words):
            destination = words[idx + 1]


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

You are an autonomous Flight Booking Orchestrator.

Your primary objective is to successfully complete the user's travel request from start to finish by intelligently coordinating specialized worker tools.

You have access to multiple worker tools. Each worker performs a specific task. The workers do not make decisions—you are responsible for all planning, coordination, sequencing, and decision-making.

Your responsibilities are:

- Understand the user's intent and determine the overall objective.
- Break the objective into the required subtasks.
- Decide which worker should be executed next based on the current conversation and available information.
- Invoke only the worker that is appropriate for the current step.
- Analyze the output returned by each worker before deciding the next action.
- Maintain context throughout the conversation and continue from the current workflow instead of restarting.
- Skip workers that are not required.
- If required information is missing, obtain it using an appropriate worker or ask the user only when no worker can provide it.
- Continue reasoning and coordinating workers until the user's request has been completely fulfilled.
- Once the objective has been achieved, provide a clear and concise final response to the user.

General Rules:

- Never assume an execution order.
- Dynamically determine the workflow based on the user's request and the information currently available.
- Use as many or as few workers as necessary.
- Base every decision on the current state of the conversation and previous worker outputs.
- Do not repeat work that has already been completed.
- Treat every worker as an independent specialist responsible only for its assigned task.
- You are the orchestrator responsible for planning, coordination, and execution of the overall workflow.

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