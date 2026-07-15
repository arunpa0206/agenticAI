# ============================================================
# FLIGHT BOOKING ORCHESTRATOR WITH EVALUATION PIPELINE
# ============================================================

import os
import sys
import uuid
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

# Ensure stdout uses UTF-8 to prevent unicode encoding issues on Windows console (e.g. for ₹ symbol)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Load environmental variables and ensure ANTHROPIC_API_KEY is defined
load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

# Import modular tools
from search_flight import search_flight
from another_flight import another_flight
from process_payment import process_payment


# ============================================================
# MODEL INSTANTIATION
# ============================================================

def create_model():
    """
    Instantiates ChatAnthropic LLM.
    """
    return ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-sonnet-5"
    )


# ============================================================
# CREATE DEEP AGENT
# ============================================================

def create_agent(model):
    """
    Sets up the main orchestrator agent with tools, prompt and checkpoint memory.
    """
    system_prompt = """
Rules:

Show only ONE flight

another
next
change

= different flight

yes
book
proceed

= process_payment

Replace old flight completely

Never show history
"""
    return create_deep_agent(
        model=model,
        tools=[
            search_flight,
            another_flight,
            process_payment
        ],
        system_prompt=system_prompt,
        checkpointer=MemorySaver()
    )


# ============================================================
# AGENT LOOP EXECUTION
# ============================================================

def run_agent(agent=None):
    """
    Chat loop orchestrating user inputs, session config, and invoking the agent.
    """
    if agent is None:
        model = create_model()
        agent = create_agent(model)

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        try:
            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                },
                config=config
            )
            print("\nAssistant:\n")
            print(result["messages"][-1].content)
        except Exception as e:
            print("\nError:", str(e))


# ============================================================
# ENTRY POINT ORCHESTRATION
# ============================================================

def main():
    """
    Main orchestration entry point.
    """
    model = create_model()
    agent = create_agent(model)
    run_agent(agent)


if __name__ == "__main__":
    main()