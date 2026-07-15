# ====================================================
# STATE MANAGEMENT
# ====================================================

import json
import os

# Define path configurations for workflow state persistence
STATE_FOLDER = "workflow_state"
STATE_FILE = f"{STATE_FOLDER}/state.json"

# Ensure the state folder exists
os.makedirs(STATE_FOLDER, exist_ok=True)

# Default blueprint for a new flight booking session state
DEFAULT_STATE = {
    "current_step": None,
    "travel_plan": {},
    "customer": {},
    "payment_status": "NOT_PAID"
}


# ====================================================
# SAVE STATE
# ====================================================

def save_state(state):
    """
    Saves the current dictionary representation of the workflow state
    to the state.json persistence file.
    """
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)


# ====================================================
# LOAD STATE
# ====================================================

def load_state():
    """
    Loads the persistent workflow state from state.json.
    Initializes state.json with DEFAULT_STATE if the file does not exist.
    """
    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# ====================================================
# FLIGHT DATA SEED
# ====================================================

# Seed data representing available flight options for matching
flights = [
    {
        "flight_id": "AI101",
        "airline": "Air India",
        "time": "10:30 AM",
        "price": "₹5200"
    },
    {
        "flight_id": "6E202",
        "airline": "IndiGo",
        "time": "2:15 PM",
        "price": "₹4300"
    },
    {
        "flight_id": "UK303",
        "airline": "Vistara",
        "time": "8:00 PM",
        "price": "₹7200"
    }
]
