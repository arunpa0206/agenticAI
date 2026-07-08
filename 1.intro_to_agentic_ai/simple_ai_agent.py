import anthropic
import random
import difflib


# ============================================================
# CLAUDE
# ============================================================

client = anthropic.Anthropic(
    api_key="YOUR_API_KEY"
)

current_flight = None


# ============================================================
# FLIGHT DATABASE
# ============================================================

flights = [

{
    "flight_id":"FL101",
    "airline":"IndiGo",
    "from":"Bangalore",
    "to":"Delhi",
    "time":"6:30 PM",
    "price":5200
},

{
    "flight_id":"FL202",
    "airline":"Air India",
    "from":"Bangalore",
    "to":"Delhi",
    "time":"8:15 PM",
    "price":6100
},

{
    "flight_id":"FL303",
    "airline":"Vistara",
    "from":"Bangalore",
    "to":"Delhi",
    "time":"9:45 PM",
    "price":5700
}

]


# ============================================================
# NORMALIZE
# ============================================================

def normalize(city):

    city = city.lower().strip()

    matches = difflib.get_close_matches(
        city,
        ["bangalore", "delhi"],
        n=1,
        cutoff=0.6
    )

    return matches[0] if matches else city


# ============================================================
# SEARCH FLIGHTS
# ============================================================

def search_flights(source, destination):

    source = normalize(source)
    destination = normalize(destination)

    matches = []

    for flight in flights:

        if (
            flight["from"].lower() == source
            and
            flight["to"].lower() == destination
        ):

            matches.append(flight)

    if not matches:
        return None

    return random.choice(matches)


# ============================================================
# BOOK FLIGHT
# ============================================================

def book_flight(flight_id):

    return {

        "booking_id":
        f"BK{random.randint(1000,9999)}",

        "flight_id":
        flight_id
    }


# ============================================================
# CANCEL FLIGHT
# ============================================================

def cancel_flight(flight_id):

    return {

        "flight_id":
        flight_id
    }


# ============================================================
# AI AGENT
# ============================================================

def ai_agent(user_input):

    global current_flight

    context = ""

    if current_flight:

        context = f"""

Current Flight:

Flight ID:
{current_flight["flight_id"]}

From:
{current_flight["from"]}

To:
{current_flight["to"]}

"""


    prompt = f"""
You are an AI Flight Assistant.

Decide user action.

Actions:

SEARCH
BOOK
CANCEL
ANOTHER

SEARCH format:
SEARCH|source|destination

BOOK format:
BOOK

CANCEL format:
CANCEL

ANOTHER format:
ANOTHER

{context}

User:
{user_input}
"""


    response = client.messages.create(

        model="claude-sonnet-4-20250514",

        max_tokens=100,

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )


    decision = response.content[0].text.strip()


    # SEARCH

    if decision.startswith("SEARCH"):

        _, source, destination = decision.split("|")

        result = search_flights(
            source,
            destination
        )

        if not result:
            return "No flights found"

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


    # BOOK

    elif decision == "BOOK":

        if not current_flight:
            return "No flight selected"

        result = book_flight(
            current_flight["flight_id"]
        )

        return f"""
==================================================
Booking Confirmed
==================================================

Booking ID : {result['booking_id']}
Flight ID  : {result['flight_id']}
"""


    # CANCEL

    elif decision == "CANCEL":

        if not current_flight:
            return "No flight selected"

        result = cancel_flight(
            current_flight["flight_id"]
        )

        return f"""
==================================================
Booking Cancelled
==================================================

Flight ID : {result['flight_id']}
"""


    # ANOTHER

    elif decision == "ANOTHER":

        if not current_flight:
            return "No current flight"

        result = search_flights(
            current_flight["from"],
            current_flight["to"]
        )

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
"""


    return "Could not understand request"