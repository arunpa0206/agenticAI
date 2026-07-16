# ====================================================
# FLIGHT BOOKING AGENT ORCHESTRATOR
# ====================================================

import os
import sys
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic

# Reconfigure stdout to use UTF-8 to prevent UnicodeEncodeErrors on Windows console (e.g. for ₹ symbol)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Load environmental variables and ensure ANTHROPIC_API_KEY is defined
load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

# Import modular tools
from tools.generate_plan import generate_plan
from tools.confirm_ticket import confirm_ticket


# ====================================================
# MODEL INSTANTIATION
# ====================================================

def create_model():
    """
    Creates and returns the ChatAnthropic model instance configured with the API key.
    """
    return ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-sonnet-5"
    )


# ====================================================
# CREATE DEEP AGENT
# ====================================================

def create_agent(model):
    """
    Instantiates the Deep Agent wrapping the language model, tools, and system prompt.
    """
    return create_deep_agent(
        model=model,
        tools=[
            generate_plan,
            confirm_ticket
        ],
        system_prompt="""

You are a Flight Assistant.

If user asks for flight:

call generate_plan()

If user says:

book
confirm
proceed

collect:

customer_name
phone

then call:

confirm_ticket()

"""
    )


# ====================================================
# AGENT LOOP EXECUTION
# ====================================================

def run_agent(agent=None):
    """
    Runs the main agent interactive chat loop.
    Supports injecting an agent, or automatically creates one if not provided.
    """
    if agent is None:
        model = create_model()
        agent = create_agent(model)

    conversation = []

    while True:
        # Prompt user input
        query = input(
            "\nYou: "
        )

        # Handle loop exit signals
        if query.lower() in ["exit", "quit"]:
            print(
                "\nGoodbye!"
            )
            break

        # Record user query
        conversation.append(
            {
                "role": "user",
                "content": query
            }
        )

        # Invoke the agent model with conversation context
        response = agent.invoke(
            {
                "messages": conversation
            }
        )

        # Extract the latest response from the agent
        msg = response["messages"][-1]

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

        # Record agent response
        conversation.append(
            {
                "role": "assistant",
                "content": msg.content
            }
        )


# ====================================================
# ENTRY POINT ORCHESTRATION
# ====================================================

def start_agent():
    """
    Main runner script instantiating all components and starting the agent loop.
    """
    model = create_model()
    agent = create_agent(model)
    run_agent(agent)