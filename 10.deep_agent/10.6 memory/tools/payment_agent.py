# payment_agent.py
# Payment Agent

def payment_agent(payment_context):

    print("\n" + "=" * 60)
    print("PAYMENT AGENT")
    print("=" * 60)

    print(
        "\nUsing payment context:\n"
    )

    print(payment_context)

    payment = input(
        "\nType 'pay' to complete payment: "
    )

    if payment.lower() != "pay":

        raise Exception(
            "Payment Failed"
        )

    booking_details = {

        "booking_status":
        "CONFIRMED",

        "flight":
        payment_context
    }

    return booking_details