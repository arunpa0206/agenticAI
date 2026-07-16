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
   - The program sets the system output encoding to UTF-8 to prevent Windows rendering crashes.
   - The LLM configuration establishes connection to Claude Sonnet.
   - The Deep Agent is created and initialized with the four modularized tools: `search_flights`, `search_hotels`, `book_flight`, and `cancel_booking`.

2. **User Input Phase**:
   - The system enters the interactive prompt loop (`run_agent`), prompting the user with `You: `.
   - The user submits their travel request (e.g., *"Help me plan a vacation to Delhi"*).

3. **Agent Evaluation & Tool Call**:
   - The user query is stored in the local conversation state and passed to the agent.
   - Claude reviews the vacation request and decides to call multiple tools to compile a plan:
     - First, it calls `search_flights(source, destination)` to retrieve flight options.
     - Second, it calls `search_hotels(city)` to fetch hotel listings for the vacation.

4. **Tool Execution**:
   - The modular tools are imported and run:
     - `search_flights.py` generates a random flight ID, flight type, price, and duration.
     - `search_hotels.py` returns a curated hotel name, rating, and price per night.
   - The outputs are returned back to the agent's running sequence context.

5. **Response Synthesis**:
   - The agent integrates the flight and hotel details together, formulating a unified vacation package.
   - The final formatted response is printed to the console.
   - The response is appended to the message history to preserve context for the next turn.

6. **Loop Progression**:
   - The process repeats for subsequent prompts (e.g., confirming the booking using `book_flight` or canceling with `cancel_booking`) until the user types `exit`.

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
                |    Deep Agent    |
                |   Planner Node   |
                +------------------+
                          |
                          v
                +------------------+
                | Execute Planning |
                | tools to search &|
                | book flights     |
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
