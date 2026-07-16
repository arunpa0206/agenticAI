import random
import os
import sys
from dotenv import load_dotenv

# Import LangChain tools and LangAnthropic models
from langchain.tools import tool
from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic

# Load environment variables
load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")


# Import modularized tools from the tools sub-package
from tools.search_flights import search_flights
from tools.search_hotels import search_hotels
from tools.book_flight import book_flight
from tools.cancel_booking import cancel_booking


# ============================================================
# MODEL & AGENT CREATION HELPERS
# ============================================================

def create_model():
    """
    Instantiates the Claude Anthropic LLM model with the API key loaded from the environment.
    """
    return ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-sonnet-5"
    )


def create_agent(model):
    """
    Creates and configures the Deep Agent instance with the tools and system prompts.
    """
    return create_deep_agent(
        model=model,
        tools=[
            search_flights,
            search_hotels,
            book_flight,
            cancel_booking
        ],
        system_prompt="""
You are a Vacation Planning and Flight Deep Agent.

Responsibilities:
- Help users plan complete vacations by searching for flights (using search_flights) and searching for hotels (using search_hotels) at their destination.
- Help users confirm/book flights using the book_flight tool.
- Help users cancel bookings using the cancel_booking tool.
- Integrate flight and hotel options to present a complete vacation package when asked to plan a trip/vacation.
- Preserve context across conversation turns and follow up naturally.

Guidelines:
- Do not show numbered menus.
- Do not invent flight IDs, hotel details, or booking IDs; always call tools to generate them.
- Present travel options and confirmation statuses clearly.
"""
    )


# ============================================================
# RUN AGENT LOOP
# ============================================================

def run_agent(agent=None):
    """
    Executes the interactive chat loop with the agent, supporting backward compatibility
    if called without arguments by creating its own model and agent.
    """
    if agent is None:
        model = create_model()
        agent = create_agent(model)

    conversation = []

    while True:
        user_query = input("\nYou: ")

        if user_query.lower() in {"exit", "quit"}:
            print("\nGoodbye!")
            break

        conversation.append({
            "role": "user",
            "content": user_query
        })

        # Invoke the agent with the conversation history
        response = agent.invoke({
            "messages": conversation
        })

        final_message = response["messages"][-1]

        print("\nAgent:")
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

        conversation.append({
            "role": "assistant",
            "content": final_message.content
        })


# ============================================================
# ENTRY POINT
# ============================================================

def start_agent():
    """
    Main entry point function. Configures standard output console encoding to UTF-8
    to prevent UnicodeEncodeError in Windows, builds the agent components, and starts the loop.
    """
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    model = create_model()
    agent = create_agent(model)
    run_agent(agent)