from planning import run_flight_planner
import asyncio


# ============================================================
# APPLICATION START
# ============================================================

print("\n========== FLIGHT PLANNER ==========\n")


# ============================================================
# START ASYNC PROGRAM
# ============================================================

asyncio.run(
    run_flight_planner()
)