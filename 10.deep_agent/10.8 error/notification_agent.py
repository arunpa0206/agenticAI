# notification_agent.py

import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from langchain_anthropic import ChatAnthropic


llm = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-sonnet-5"
)


def success_notification(
    booking_details
):

    prompt = f"""
Generate booking confirmation.

{booking_details}
"""

    response = llm.invoke(
        prompt
    )

    return response.content


def failure_notification():

    return (
        "Flight booking could "
        "not be completed."
    )