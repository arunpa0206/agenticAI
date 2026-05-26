# seat_selection.py

from langchain.tools import tool

@tool
def select_seat():

    """
    Select seat.
    """

    print("=" * 70)
    print("TASK 3 → SEAT SELECTION")
    print("=" * 70)

    print("\nAvailable Seats:\n")

    print("A1 A2 A3")
    print("B1 B2 B3")
    print("C1 C2 C3")

    seat = input(
        "\nChoose seat: "
    )

    return seat