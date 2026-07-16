# Setup

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Add your API key

Ensure your `ANTHROPIC_API_KEY` is set in the root `.env` file.

3. Activate Virtual Environment (PowerShell)

Depending on your current working directory in the terminal, run:
* **From the project root (`o:\training_arun`):**
  ```powershell
  .\agentenv\Scripts\Activate.ps1
  ```
* **From the `10.deep_agent` directory:**
  ```powershell
  ..\agentenv\Scripts\Activate.ps1
  ```
* **From this specific project directory:**
  ```powershell
  ..\..\agentenv\Scripts\Activate.ps1
  ```

4. Run the project

```bash
python main.py
```

---

## Sequence of Events (Text Form)

1. **Startup**:
   - The user executes `main.py`, which prints the greeting header and invokes `start_agent()`.
   - The program sets the system output encoding to UTF-8.
   - The Deep Agent is created and initialized with four decomposed, task-specific tools: `search_flights`, `enter_passenger_details`, `select_seat`, and `payment_confirmation`.

2. **User Input Phase**:
   - The system enters the interactive prompt loop (`run_agent`), prompting the user with `You: `.
   - The user enters a compound booking request (e.g., *"Search for a flight from Mumbai to Delhi, book it for John, choose seat 14C, and confirm payment"*).

3. **Task Decomposition & Tool Selection**:
   - The user query is stored and analyzed by the agent.
   - Instead of running a hardcoded procedural pipeline, the agent dynamically decomposes the compound request into logical steps:
     1. Calls `search_flights` to search for available routes.
     2. Calls `enter_passenger_details` to log the passenger's name.
     3. Calls `select_seat` to assign the preferred seat.
     4. Calls `payment_confirmation` to finalize the payment status.

4. **Iterative Tool Execution**:
   - The agent executes each tool in sequence:
     - `tools/search.py` returns matching flight numbers and routes.
     - `tools/passenger_details.py` registers the passenger details.
     - `tools/seat_selection.py` allocates the selected seat.
     - `tools/payment_confirmation.py` updates the status to confirmed.
   - If any parameter is missing (e.g., if the user forgot to specify a seat), the agent detects the gap and asks the user for clarification rather than failing.

5. **Response Synthesis**:
   - The final confirmation, showing the completed booking, passenger details, seat number, and payment status, is printed.
   - The conversation context is preserved to handle any follow-up actions (such as changing seats or booking another ticket).

---

## Code Execution Flow

```text
                +------------------+
                |   Start Program  |
                +------------------+
                          |
                          v
                +------------------+
                | User Enters Query|
                +------------------+
                          |
                          v
                +------------------+
                | Task Decomposing |
                | Split query into |
                | steps (search,   |
                | details, book)   |
                +------------------+
                          |
                          v
                +------------------+
                | Execute step by  |
                | step in sequence |
                +------------------+
                          |
                          v
                +------------------+
                | Display Response |
                +------------------+
                          |
                          v
                         End
```
