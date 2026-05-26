# booking_worker.py

from langchain.tools import tool


@tool
def booking_worker():

    """
    Collect passenger details,
    process seat selection,
    and simulate payment.
    """

    print(
        "\nPassenger Details\n"
    )

    passenger = input(
        "Name: "
    )

    phone = input(
        "Phone: "
    )

    print("\nAvailable Seats:\n")

    print("A1 A2 A3")
    print("B1 B2 B3")
    print("C1 C2 C3")


    seat = input(
        "\nSeat: "
    )

    payment = input(
        "\nType pay: "
    )

    if payment.lower() != "pay":

        return {

            "status":
            "FAILED"
        }


    return {

        "passenger":
        passenger,

        "phone":
        phone,

        "seat":
        seat,

        "payment":
        "SUCCESS",

        "status":
        "CONFIRMED"
    }