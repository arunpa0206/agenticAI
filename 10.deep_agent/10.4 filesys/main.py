
"""Here is the entire end-to-end workflow from the moment you run the program in `10.4 filesys`:

### 1. Process Startup
* You run the command:
  ```powershell
  ..\..\agentenv\Scripts\python.exe main.py
  ```
* **[main.py](file:///o:/training_arun/10.deep_agent/10.4%20filesys/main.py)** launches, prints the banner, imports `main()` from **[planning.py](file:///o:/training_arun/10.deep_agent/10.4%20filesys/planning.py)**, and executes it.
* The `main()` function:
  1. Loads environment variables (like `ANTHROPIC_API_KEY`).
  2. Instantiates the Claude model.
  3. Creates the Deep Agent registering two tools: `generate_flight_plan` and `confirm_ticket`.
  4. Starts the interactive chat loop (`run_agent`).

---

### 2. Flight Searching
* **User Input**: You type: *"Show me flights from Bangalore to Delhi."*
* **Agent Decision**: The agent determines you want to plan a flight and calls the **`generate_flight_plan()`** tool.
* **State Update**:
  1. The tool randomly selects a flight option.
  2. It reads `workflow_state/state.json`.
  3. It saves the flight details, resets the customer details to empty, sets `payment_status` to `"NOT_PAID"`, and saves.
* **Agent Response**: The agent displays the flight option and asks you for passenger details and payment confirmation to finalize the ticket.

---

### 3. Booking Details & Payment
* **User Input**: You type: *"Book it for John Doe, phone 123-456-7890. Payment is completed."*
* **Agent Decision**: The agent extracts the passenger name, phone, and payment status, and calls the **`confirm_ticket()`** tool.

---

### 4. Ticket Confirmation & File Export
* **State Update**:
  1. The tool loads `state.json` and checks if `payment_confirmed` is `True`.
  2. It saves the passenger details and updates the status to `"PAID"`.
  3. It writes the updated state back to `state.json`.
* **Filesystem Export**: 
  * The tool calls `FileService.create_external_records(state)` in **[filesys.py](file:///o:/training_arun/10.deep_agent/10.4%20filesys/filesys.py)**.
  * This service exports three files into the `external_storage/` directory:
    * **`ticket.txt`**: A readable text board pass format.
    * **`ticket.json`**: A structured JSON record of the booking.
    * **`bookings.csv`**: A CSV row containing the booking details added to a global ledger sheet.

---

### 5. Completion
* **Agent Response**: The tool returns success to the agent, and the agent outputs: *"Booking confirmed and files created."* 
* The session remains active for further requests, or you can type `exit` to quit."""

# ====================================================
# APPLICATION STARTUP ENTRYPOINT
# ====================================================

from planning import start_agent


# ====================================================
# APPLICATION START
# ====================================================

print("=" * 70)
print("DEEP FLIGHT AGENT - FILESYSTEM STORAGE")
print("=" * 70)


# ====================================================
# START AGENT
# ====================================================

if __name__ == "__main__":
    start_agent()