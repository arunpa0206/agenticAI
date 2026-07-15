# ============================================================
# FLIGHT BOOKING ORCHESTRATOR WITH CONTEXT MANAGEMENT
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
from tools.search_flight import search_flight
from tools.another_flight import another_flight
from tools.make_payment import make_payment
from tools.send_confirmation import send_confirmation


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
You are a flight booking assistant.

Rules:
- Show ONE flight at a time
- Never list multiple flights

If user says:
another, next, different, change flight, new flight
call another_flight()
Replace old flight completely

If user says:
yes, proceed, book
call make_payment()

After payment:
call send_confirmation()

Never invent flights. Use only tool results.
"""
    memory = MemorySaver()
    return create_deep_agent(
        model=model,
        tools=[
            search_flight,
            another_flight,
            make_payment,
            send_confirmation
        ],
        system_prompt=system_prompt,
        checkpointer=memory
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
            "thread_id": f"session-{uuid.uuid4()}"
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
            print("\nAssistant:")
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