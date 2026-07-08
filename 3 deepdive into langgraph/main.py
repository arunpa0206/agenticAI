from langgraph_flow import app

print("=" * 60)
print("AI Flight Assistant")
print("=" * 60)

while True:

    user = input("\nYou: ")

    if user.lower() in ["exit", "quit"]:
        break

    result = app.invoke(
        {
            "user_input": user
        }
    )

    print("\nAgent:", result["response"])