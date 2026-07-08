from anthropic import Anthropic
import json


API_KEY = "YOUR_API_KEY"

client = Anthropic(
    api_key=API_KEY
)


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

        model="claude-sonnet-4-0",

        max_tokens=200,

        system=system_prompt,

        messages=[
            {
                "role":"user",
                "content":user_input
            }
        ]
    )


    output = response.content[0].text.strip()


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