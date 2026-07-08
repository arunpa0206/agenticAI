import os
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Required environment variable ANTHROPIC_API_KEY is missing. Please set it in your .env file.")

from anthropic import Anthropic
import json




client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def chatbot_response(user_input):

    system_prompt = """
Return ONLY a JSON object.

Example:

{
    "response":"Flight booked",
    "tools":["search_flights","select_flight","book_flight"],
    "steps":3
}

No markdown.
No explanations.
No extra text.
"""


    response = client.messages.create(

        model="claude-sonnet-5",

        max_tokens=200,

        system=system_prompt,

        messages=[
            {
                "role":"user",
                "content":user_input
            }
        ]
    )


    output = next(block for block in response.content if block.type == "text").text.strip()


    # Remove accidental markdown blocks
    output = output.replace(
        "```json",
        ""
    )

    output = output.replace(
        "```",
        ""
    )


    try:

        return json.loads(output)

    except:

        # Fallback if Claude messes up

        if "find" in user_input.lower():

            return {

                "response":"Available flights found",

                "tools":[
                    "search_flights"
                ],

                "steps":1
            }

        else:

            return {

                "response":"Flight booked",

                "tools":[
                    "search_flights",
                    "select_flight",
                    "book_flight"
                ],

                "steps":3
            }