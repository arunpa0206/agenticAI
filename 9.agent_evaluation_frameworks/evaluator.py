def detect_intent(user_input):
    # Detect the user's intent from the input
    if "find" in user_input.lower():
        detected_intent = "flight_search"
    else:
        detected_intent = "flight_booking"

    return detected_intent


def find_golden_record(detected_intent, golden_dataset):
    # Find the matching record in the golden dataset
    golden_record = None

    for record in golden_dataset:
        if record["intent"] == detected_intent:
            golden_record = record
            break

    return golden_record


def initialize_results(detected_intent, results, golden_record=None):
    # Initialize the metrics for this intent if it doesn't already exist
    if detected_intent not in results:
        results[detected_intent] = {
            "success_total": 0,
            "tool_total": 0,
            "step_total": 0,
            "policy_total": 0,
            "count": 0,
            "thresholds": golden_record.get("thresholds") if golden_record else None
        }


def calculate_metrics(
    golden_record,
    detected_intent,
    agent_prediction,
):
    # Extract the agent's output
    agent_response = agent_prediction["response"]
    used_tools = agent_prediction["tools"]
    reasoning_steps = agent_prediction["steps"]

    # Calculate Success Score
    success_score = 0

    if golden_record["expected_output"].lower() in agent_response.lower():
        success_score = 100

    # Calculate Tool Accuracy
    matched_tools = len(
        set(used_tools) &
        set(golden_record["expected_tools"])
    )

    tool_accuracy = (
        matched_tools /
        len(golden_record["expected_tools"])
    ) * 100

    # Calculate Policy Score
    policy_score = 100

    if (
        detected_intent == "flight_booking"
        and
        "search_flights" not in used_tools
    ):
        policy_score = 0

    return (
        success_score,
        tool_accuracy,
        reasoning_steps,
        policy_score,
    )


def update_results(
    detected_intent,
    results,
    success_score,
    tool_accuracy,
    reasoning_steps,
    policy_score,
):
    # Add the current metrics to the accumulated totals
    results[detected_intent]["success_total"] += success_score
    results[detected_intent]["tool_total"] += tool_accuracy
    results[detected_intent]["step_total"] += reasoning_steps
    results[detected_intent]["policy_total"] += policy_score
    results[detected_intent]["count"] += 1


def evaluate_metrics(
    user_input,
    agent_prediction,
    golden_dataset,
    results,
):
    # Step 1: Detect the user's intent
    detected_intent = detect_intent(user_input)

    # Step 2: Find the matching record in the golden dataset
    golden_record = find_golden_record(
        detected_intent,
        golden_dataset,
    )

    # Step 3: Initialize the metrics for this intent
    initialize_results(
        detected_intent,
        results,
        golden_record,
    )

    # Step 4: Calculate the evaluation metrics
    (
        success_score,
        tool_accuracy,
        reasoning_steps,
        policy_score,
    ) = calculate_metrics(
        golden_record,
        detected_intent,
        agent_prediction,
    )

    # Step 5: Update the accumulated metrics
    update_results(
        detected_intent,
        results,
        success_score,
        tool_accuracy,
        reasoning_steps,
        policy_score,
    )