from langgraph_flow import app

print("=" * 60)
print("AI Flight Planning Agent")
print("=" * 60)

while True:
    user_query = input("\nYou: ")

    if user_query.lower() in ["exit", "quit"]:
        print("\nGoodbye!")
        break

    result = app.invoke({
        "user_input": user_query
    })

    print("\nAgent:", result["response"])
