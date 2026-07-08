def payment_workflow(
    approved_flight
):

    print("="*70)

    print(
        "PAYMENT WORKFLOW"
    )

    print("="*70)


    print(

        f"\nProcessing payment "
        f"for "

        f"{approved_flight['flight_id']}"

    )


    return {

        "payment_status":
        "SUCCESS"

    }