from langchain_flow import app

while True:

    user = input("\nYou: ")

    if user.lower() in ["exit", "quit"]:
        print("\nGoodbye!")
        break

    # Invoke the graph
    app.invoke(
        {
            "user_input": user
        }
    )