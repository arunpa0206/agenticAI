# ============================================================
# TOOL: PROCESS PAYMENT
# ============================================================

import time
import random
from langchain_core.tools import tool
from state import conversation_state
from evaluation import evaluate_workflow, display_metrics


@tool
def process_payment() -> str:
    """
    Simulates payment processing, evaluates workflow metrics, and prints the result.
    """
    flight = conversation_state["current_flight"]

    print("\n[PAYMENT AGENT]")
    time.sleep(2)

    # 20% failure rate simulation
    if random.random() < 0.2:
        payment_result = {"status": "FAILED"}
    else:
        payment_result = {"status": "SUCCESS"}

    conversation_state["payment_result"] = payment_result

    confirmation = (
        f"\nBOOKING RESULT\n"
        f"----------------------\n"
        f"Flight : {flight['flight_id']}\n"
        f"Status : {payment_result['status']}\n"
    )

    total_time = time.time() - conversation_state["start_time"]

    # Calculate metrics
    metrics = evaluate_workflow(
        payment_result=payment_result,
        total_time=total_time,
        user_query=f"{flight['from']} to {flight['to']}",
        assistant_output=confirmation,
        tool_calls=3,
        failed_tools=0,
        retries=0
    )

    # Display compiled metrics
    display_metrics(metrics)

    return confirmation
