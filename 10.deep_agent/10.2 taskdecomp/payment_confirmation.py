# payment_confirmation.py

from langchain.tools import tool

@tool
def payment_confirmation():

    """
    Process payment.
    """

    print("=" * 70)
    print("TASK 4 → PAYMENT")
    print("=" * 70)

    payment = input(
        "\nType 'pay': "
    )

    if payment.lower() != "pay":

        return (
            "Payment failed"
        )

    return (
        "Payment successful"
    )