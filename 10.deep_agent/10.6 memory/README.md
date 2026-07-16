# Setup

First Turn: Search Flight
User Input: You type: "Show me flights from Bangalore to Delhi."
Agent Invoke: The loop calls agent.invoke() passing only your current message and the config containing the unique thread_id.
Execution:
The agent triggers the search_flight tool to retrieve a flight option.
The tool returns a flight.
The MemorySaver automatically saves this state (the flight and conversation logs) on the thread checkpoint.
Agent Response: The agent displays the flight option (e.g. FL101) to you.

Second Turn: Different Options (Memory Recall)
User Input: You type: "Show me another option."
Agent Invoke: The loop calls agent.invoke() passing only your new message "Show me another option" and the same thread_id.
Execution:
Because of the thread_id, the agent's checkpointer automatically loads the complete context history of the previous turn.
The agent remembers the source and destination (Bangalore 
→
→ Delhi) and the last flight offered (FL101).
The agent calls another_flight(), which generates a different flight option (e.g. FL102).
The checkpointer saves the new state.
Agent Response: The agent displays the new flight option.

Third Turn: Booking and Payment
User Input: You type: "Yes, book it."
Agent Invoke: The loop calls agent.invoke() with the same thread_id.
Execution:
The agent recalls the currently selected flight (FL102) from thread memory.
The agent calls make_payment() to process mock payment.
The checkpointer saves the paid status.
Agent Response: The agent displays a successful payment confirmation.

Final Confirmation
Agent Autonomous Call: Right after payment succeeds, the agent's system prompt triggers it to immediately call the send_confirmation() tool.
Execution:
The tool loads the customer details and flight data from memory history.
It prints a final confirmation receipt card.
Agent Response: The agent displays the receipt to complete the workflow.

1. Install dependencies

pip install -r requirements.txt


2. Add your API key

Open the project files and replace:

api_key="YOUR_API_KEY"

with your own Anthropic API key.


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
                | Context Agent    |
                | Prepares context |
                +------------------+
                          |
                          v
                +------------------+
                | Pass context to  |
                | sub-agents       |
                +------------------+
                          |
                          v
                +------------------+
                | Search -> Payment|
                | -> Notification  |
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
