from langgraph_flow import app

# ============================================================
# Store Current Flight
# ============================================================

current_flight_id = "FL101"

# ============================================================
# Main Loop
# ============================================================

print("=" * 60)
print("AI Flight Planning Agent")
print("=" * 60)

while True:

    user_query = input("\nYou: ")

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if user_query.lower() in ["exit", "quit"]:

        print("\nGoodbye!")
        break

    # --------------------------------------------------------
    # OPTION 1 = CONFIRM
    # --------------------------------------------------------

    elif user_query.strip() == "1":

        result = app.invoke({
            "user_input": f"Book flight {current_flight_id}"
        })

    # --------------------------------------------------------
    # OPTION 2 = NEW PLAN
    # --------------------------------------------------------

    elif user_query.strip() == "2":

        result = app.invoke({
            "user_input": "Search flight from Bangalore to Delhi"
        })

    # --------------------------------------------------------
    # OPTION 3 = CANCEL
    # --------------------------------------------------------

    elif user_query.strip() == "3":

        result = app.invoke({
            "user_input": f"Cancel flight {current_flight_id}"
        })

    # --------------------------------------------------------
    # NORMAL USER QUERY
    # --------------------------------------------------------

    else:

        result = app.invoke({
            "user_input": user_query
        })

    print("\nAgent:", result["response"])