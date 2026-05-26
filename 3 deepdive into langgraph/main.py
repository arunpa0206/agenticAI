from langgraph_flow import app
import langgraph_flow

print("="*60)
print("AI Flight Assistant")
print("="*60)

while True:

    user=input("\nYou: ")

    if user.lower() in [
        "exit",
        "quit"
    ]:

        break


    if user=="1":

        if langgraph_flow.current_flight:

            flight=langgraph_flow.current_flight

            user=(
                f"Search flight from "
                f"{flight['from']} "
                f"to "
                f"{flight['to']}"
            )


    elif user=="2":

        if langgraph_flow.current_flight:

            flight=langgraph_flow.current_flight

            user=(
                f"Book flight "
                f"{flight['flight_id']}"
            )


    elif user=="3":

        if langgraph_flow.current_flight:

            flight=langgraph_flow.current_flight

            user=(
                f"Cancel flight "
                f"{flight['flight_id']}"
            )


    result=app.invoke(
        {
            "user_input":user
        }
    )

    print(
        "\nAgent:",
        result["response"]
    )