# ====================================================
# TOOL: GENERATE FLIGHT PLAN
# ====================================================

import random
from langchain.tools import tool
from .state import load_state, save_state, flights


@tool
def generate_plan():
    """
    Generate a random flight plan from Bangalore to Delhi,
    saves it to the persistent state, and transitions the step.
    """
    # Select a random flight from the database seed
    selected = random.choice(flights)
    
    # Load and update the persistent state
    state = load_state()
    state["travel_plan"] = {
        "source": "Bangalore",
        "destination": "Delhi",
        **selected
    }
    state["current_step"] = "PLAN_GENERATED"
    
    # Persist back the modified state
    save_state(state)
    
    return selected
