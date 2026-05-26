from simple_ai_agent import ai_agent


print("="*60)
print("AI Flight Assistant")
print("="*60)


while True:

    query = input("\nYou: ")

    if query.lower() == "exit":
        break

    response = ai_agent(query)

    print("\nAgent:", response)