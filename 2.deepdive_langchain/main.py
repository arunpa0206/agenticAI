from langchain_flow import app
import langchain_flow

print("="*60)
print("AI Flight Assistant")
print("="*60)

while True:

    user=input("\nYou: ")

    if user.lower() in ["exit","quit"]:

        print("\nGoodbye!")
        break


    # Generate New Flight
    if user=="1":

        if langchain_flow.current_flight:

            current=langchain_flow.current_flight

            user=(
                f"Search flight from "
                f"{current['from']} "
                f"to "
                f"{current['to']}"
            )


    # Book Current Flight
    elif user=="2":

        if langchain_flow.current_flight:

            current=langchain_flow.current_flight

            user=(
                f"Book flight "
                f"{current['flight_id']}"
            )


    # Cancel Flight
    elif user=="3":

        if langchain_flow.current_flight:

            current=langchain_flow.current_flight

            user=(
                f"Cancel flight "
                f"{current['flight_id']}"
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