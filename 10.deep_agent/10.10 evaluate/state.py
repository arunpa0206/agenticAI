# ============================================================
# STATE PERSISTENCE
# ============================================================

# Global state tracking current search route, flight, payment result, and timestamp
conversation_state = {
    "source": None,
    "destination": None,
    "current_flight": None,
    "payment_result": None,
    "start_time": None
}
