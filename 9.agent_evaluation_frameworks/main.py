from agent import chatbot_response
from evaluator import evaluate_metrics, detect_intent
from output import generate_output

import json


# Load the test prompts
with open("data/test_prompts.json", "r") as file:
    test_prompts = json.load(file)

# Load the golden dataset
with open("data/golden_dataset.json", "r") as file:
    golden_dataset = json.load(file)


# Store the accumulated evaluation results
results = {}


# Evaluate each test prompt
for index, prompt in enumerate(test_prompts):

    user_input = prompt["input"]

    print(
        f"[{index + 1}/{len(test_prompts)}] "
        f"Evaluating: '{user_input}'..."
    )

    # Get the agent's prediction
    agent_prediction = chatbot_response(user_input)

    # Evaluate the prediction
    evaluate_metrics(
        user_input,
        agent_prediction,
        golden_dataset,
        results,
    )

    # Inject intent key so output.py can read it
    detected_intent = detect_intent(user_input)
    if detected_intent in results:
        results[detected_intent]["intent"] = detected_intent


# Generate the final evaluation report
generate_output(results)

print("\nEvaluation complete!")
print("Results have been written to output.json")