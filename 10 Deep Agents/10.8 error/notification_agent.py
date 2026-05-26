# notification_agent.py

from langchain_anthropic import ChatAnthropic


llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key="YOUR_API_KEY"
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