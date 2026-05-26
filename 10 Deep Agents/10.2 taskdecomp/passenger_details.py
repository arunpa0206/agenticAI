# passenger_details.py

from langchain.tools import tool

@tool
def enter_passenger_details():

    """
    Collect passenger details.
    """

    print("=" * 70)
    print("TASK 2 → ENTER DETAILS")
    print("=" * 70)

    passenger_name = input(
        "\nEnter passenger name: "
    )

    phone = input(
        "Enter phone number: "
    )

    return {

        "name":
        passenger_name,

        "phone":
        phone
    }