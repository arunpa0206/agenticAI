from langgraph_flow import app

if __name__ == "__main__":

    state = {
        "flights": [],
        "bookings": [],
    }

    while True:

        user = input("\nYou: ")

        if user.lower() in {"exit", "quit"}:
            break

        state["user_input"] = user

        state = app.invoke(state)

        print("\nAgent:")
        print(state["response"])
