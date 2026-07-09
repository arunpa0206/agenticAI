from agent import chatbot_response
from evaluator import evaluate_metrics
from output import generate_output

import json


# Load datasets

with open("data/test_prompts.json","r") as f:
    prompts=json.load(f)

with open("data/golden_dataset.json","r") as f:
    golden=json.load(f)


results={}


for i, test in enumerate(prompts):

    user_input=test["input"]
    print(f"[{i+1}/{len(prompts)}] Evaluating prompt: '{user_input}'...")


    # Get Claude prediction

    prediction=chatbot_response(
        user_input
    )


    # Send for evaluation

    evaluate_metrics(

        user_input,

        prediction,

        golden,

        results
    )


# Generate final JSON output

generate_output(
    results
)


print(
    "Output has been written to output.json file"
)