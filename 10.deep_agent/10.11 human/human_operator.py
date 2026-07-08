import json


FLIGHT_FILE=(

    "flight_options.json"

)


def wait_for_approval():

    print("="*70)

    print(
        "FLIGHT OPERATOR REVIEW"
    )

    print("="*70)


    print(

        "\nOur flight operator "
        "is reviewing flights."

    )


    print(

        "\nOpen:\n"

        "flight_options.json"

    )


    print(

        "\nApprove flights by changing:\n"

        '"approval_status":"NOT_APPROVED"\n'

        "to:\n"

        '"approval_status":"APPROVED"'

    )


    input(

        "\nPress ENTER after "
        "review is complete..."
    )


    with open(

        FLIGHT_FILE,
        "r",
        encoding="utf-8"

    ) as file:

        flights=json.load(
            file
        )


    approved=[]


    for flight in flights:

        if (

            flight[
                "approval_status"
            ]

            ==

            "APPROVED"

        ):

            approved.append(
                flight
            )


    return approved