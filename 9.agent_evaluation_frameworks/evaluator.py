def evaluate_metrics(

    user_input,
    prediction,
    golden,
    results

):


    # Detect intent

    if "find" in user_input.lower():

        intent="flight_search"

    else:

        intent="flight_booking"


    expected=None


    for item in golden:

        if item["intent"]==intent:

            expected=item
            break


    id=expected["id"]


    # Initialize values

    if id not in results:

        results[id]={

            "id":id,

            "intent":intent,

            "success_total":0,

            "tool_total":0,

            "step_total":0,

            "policy_total":0,

            "count":0
        }


    current=results[id]


    actual_response=prediction["response"]

    actual_tools=prediction["tools"]

    actual_steps=prediction["steps"]


    # Success

    success=0

    if (

        expected["expected_output"]
        .lower()

        in

        actual_response.lower()

    ):

        success=100


    # Tool Accuracy

    matched_tools=len(

        set(actual_tools)

        &

        set(expected["expected_tools"])

    )


    tool_accuracy=(

        matched_tools/

        len(expected["expected_tools"])

    )*100


    # Policy

    policy=100


    if (

        intent=="flight_booking"

        and

        "search_flights"
        not in actual_tools

    ):

        policy=0


    # Store totals

    current["success_total"]+=success

    current["tool_total"]+=tool_accuracy

    current["step_total"]+=actual_steps

    current["policy_total"]+=policy

    current["count"]+=1