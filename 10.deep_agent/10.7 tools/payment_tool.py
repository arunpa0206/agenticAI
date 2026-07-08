# payment_tool.py

import json


def payment_tool(
    selected_flight
):

    print("=" * 60)
    print("PAYMENT TOOL")
    print("=" * 60)

    payment = input(
        "\nType 'pay': "
    )

    payment_status = {}

    if payment.lower() == "pay":

        payment_status = {
            "payment_status":
            "SUCCESS"
        }

    else:

        payment_status = {
            "payment_status":
            "FAILED"
        }

        with open(
            "payment.json",
            "w"
        ) as f:

            json.dump(
                payment_status,
                f,
                indent=4
            )

        raise Exception(
            "Payment Failed"
        )

    with open(
        "payment.json",
        "w"
    ) as f:

        json.dump(
            payment_status,
            f,
            indent=4
        )

    return {

        "booking_status":
        "CONFIRMED",

        "flight":
        selected_flight
    }