from planning import ai_agent


# ============================================================
# APPLICATION START
# ============================================================

print("="*60)
print("AI Flight Assistant")
print("="*60)


# ============================================================
# MAIN CHAT LOOP
# ============================================================

while True:

    # Get user input
    query = input("\nYou: ")

    # Exit application
    if query.lower() == "exit":
        break

    # Send query to AI agent
    response = ai_agent(query)

    # Print response
    print(
        "\nAgent:",
        response
    )