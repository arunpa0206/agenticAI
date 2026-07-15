import sys
from langgraph_flow import app

# Reconfigure console standard output to use UTF-8. 
# This prevents a UnicodeEncodeError when printing currency symbols like '₹' in Windows environments.
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

if __name__ == "__main__":

    # Initialize the conversation state dictionary
    state = {
        "flights": [],
        "bookings": [],
        "response": ""
    }

    # Start the interactive chat loop
    while True:

        # Get raw text query from user
        user = input("\nYou: ")

        # Exit command check
        if user.lower() in {"exit", "quit"}:
            break

        # Save user query to state
        state["user_input"] = user

        # Invoke the compiled LangGraph application.
        # The graph will execute sequentially, starting with input_guardrail to validate the request.
        state = app.invoke(state)

        # Print the final agent response
        print("\nAgent:")
        print(state["response"])
