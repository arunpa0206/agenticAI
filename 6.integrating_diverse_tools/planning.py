import anthropic

from tools import (
    tools,
    tool_map
)

# ============================================================
# CLAUDE
# ============================================================

client = anthropic.Anthropic(
    api_key="YOUR_API_KEY"
)

conversation_history = []
current_flight = None


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI Flight Assistant.

Always use tools.

Rules:

User:
Book a flight from Bangalore to Delhi
-> search_flights

User:
book this flight
-> book_flight

User:
confirm
-> book_flight

User:
cancel this booking
-> cancel_flight

User:
show another flight
-> search_flights

If a flight already exists in context,
do NOT search again for booking requests.
"""


# ============================================================
# AGENT
# ============================================================

def ai_agent(user_input):

    global current_flight
    global conversation_history


    # Store user message
    conversation_history.append({

        "role": "user",
        "content": user_input

    })


    response = client.messages.create(

        model="claude-sonnet-4-20250514",

        max_tokens=300,

        system=SYSTEM_PROMPT,

        tools=tools,

        messages=conversation_history
    )


    # ========================================================
    # TOOL EXECUTION
    # ========================================================

    if response.stop_reason == "tool_use":

        tool = response.content[-1]

        tool_name = tool.name
        tool_input = tool.input


        # ====================================================
        # AUTO CURRENT FLIGHT HANDLING
        # ====================================================

        if current_flight:

            # Auto-book current flight
            if tool_name == "book_flight":

                tool_input = {

                    "flight_id":
                    current_flight["flight_id"]
                }


            # Auto-cancel current flight
            elif tool_name == "cancel_flight":

                tool_input = {

                    "flight_id":
                    current_flight["flight_id"]
                }


            # Another flight from same route
            elif (

                tool_name == "search_flights"
                and
                "another" in user_input.lower()

            ):

                tool_input = {

                    "source":
                    current_flight["from"],

                    "destination":
                    current_flight["to"]
                }


        # Execute tool
        result = tool_map[
            tool_name
        ](
            **tool_input
        )


        # ====================================================
        # STORE TOOL RESULT IN MEMORY
        # IMPORTANT FIX
        # ====================================================

        conversation_history.append({

            "role": "assistant",

            "content": [

                {
                    "type":"tool_use",
                    "id":tool.id,
                    "name":tool_name,
                    "input":tool_input
                }

            ]
        })


        conversation_history.append({

            "role":"user",

            "content":[

                {

                    "type":"tool_result",

                    "tool_use_id":
                    tool.id,

                    "content":
                    str(result)

                }

            ]
        })


        # ====================================================
        # SEARCH
        # ====================================================

        if tool_name == "search_flights":

            if "message" in result:

                return result["message"]


            current_flight = result

            return f"""
==================================================
Flight Found
==================================================

Flight ID : {result['flight_id']}
Airline   : {result['airline']}
Route     : {result['from']} → {result['to']}
Time      : {result['time']}
Price     : ₹{result['price']}

What would you like to do next?
"""


        # ====================================================
        # BOOK
        # ====================================================

        elif tool_name == "book_flight":

            return f"""
==================================================
Booking Confirmed
==================================================

Booking ID : {result['booking_id']}
Flight ID  : {result['flight_id']}
Status     : {result['status']}
"""


        # ====================================================
        # CANCEL
        # ====================================================

        elif tool_name == "cancel_flight":

            return f"""
==================================================
Booking Cancelled
==================================================

Flight ID : {result['flight_id']}
Status    : {result['status']}
"""


    return response.content[0].text