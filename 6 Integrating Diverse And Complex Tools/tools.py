import random
import difflib


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
# CITY NORMALIZATION
# ============================================================

def normalize(city):

    city = city.lower().strip()

    matches = difflib.get_close_matches(

        city,

        [
            "bangalore",
            "delhi"
        ],

        n=1,
        cutoff=0.6
    )

    return matches[0] if matches else city


# ============================================================
# SEARCH FLIGHTS
# ============================================================

def search_flights(
    source,
    destination
):

    source = normalize(source)

    destination = normalize(destination)

    matches = []

    for flight in flights:

        if(

            flight["from"].lower()
            ==
            source

            and

            flight["to"].lower()
            ==
            destination
        ):

            matches.append(
                flight
            )


    if not matches:

        return {

            "message":
            "No flights found"
        }


    return random.choice(
        matches
    )


# ============================================================
# BOOK FLIGHT
# ============================================================

def book_flight(
    flight_id
):

    return {

        "booking_id":
        f"BK{random.randint(1000,9999)}",

        "flight_id":
        flight_id,

        "status":
        "CONFIRMED"
    }


# ============================================================
# CANCEL FLIGHT
# ============================================================

def cancel_flight(
    flight_id
):

    return {

        "flight_id":
        flight_id,

        "status":
        "CANCELLED"
    }


# ============================================================
# TOOL MAP
# ============================================================

tool_map = {

    "search_flights":
    search_flights,

    "book_flight":
    book_flight,

    "cancel_flight":
    cancel_flight
}


# ============================================================
# TOOL DEFINITIONS
# ============================================================

tools = [

{
"name":"search_flights",

"description":"Search flights",

"input_schema":{

"type":"object",

"properties":{

"source":{
"type":"string"
},

"destination":{
"type":"string"
}

},

"required":[
"source",
"destination"
]

}

},

{
"name":"book_flight",

"description":"Book current flight",

"input_schema":{

"type":"object",

"properties":{

"flight_id":{
"type":"string"
}

},

"required":[
"flight_id"
]

}

},

{
"name":"cancel_flight",

"description":"Cancel current flight",

"input_schema":{

"type":"object",

"properties":{

"flight_id":{
"type":"string"
}

},

"required":[
"flight_id"
]

}

}

]