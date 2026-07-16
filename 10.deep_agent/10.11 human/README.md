# Setup
User Input: You type: "Plan a flight itinerary."
Agent Decision: The agent calls the generate_flights tool.
Worker Execution:
The tool searches/generates 15 random flights across different categories (premium, cheap, nonstop).
It marks every flight with approval_status = "NOT_APPROVED".
It writes the list to 
flight_options.json
Returns a search status message stating that the operator is reviewing the flight options.

Human Operator Review (Checkpoint Block)
Agent Decision: The agent immediately invokes the approval_checkpoint tool.
Console Halt:
The console displays instructions: "Open flight_options.json. Approve flights by changing 'NOT_APPROVED' to 'APPROVED'".
The code hangs at a console input block: Press ENTER after review is complete...
Human Action:
You open the generated flight_options.json file in your editor.
You manually change "approval_status": "NOT_APPROVED" to "APPROVED" for one or more flights.
You save the JSON file.
You go back to the terminal and press ENTER.

Fetching Approvals
Tool Resumes:
The checkpoint tool reads flight_options.json via get_approved_flights().
It filters out only the flights that you marked "APPROVED".
If none approved: The tool returns "We are sorry. No flights approved." and exits.
If approved: It displays the approved flight options list to the user and asks which one they want to book.

Payment & Final Receipt
User Input: You type: "Book flight number 3."
Agent Decision: The agent calls payment_workflow() to process payment.
Final Receipt: The agent calls notification_workflow() to generate and present a successful booking receipt card.

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
                | Agent Execution  |
                +------------------+
                          |
                          v
                +------------------+
                | Requires approval|
                | of transaction?  |
                +------------------+
                     /            \
                   Yes            No
                   /                \
                  v                  v
        +------------------+   +------------------+
        | Prompt Operator  |   | Auto-execute     |
        | wait_for_approval|   | booking / task   |
        +------------------+   +------------------+
                  |                  |
                  v                  v
        Confirm or Cancel
                  |                  |
                  v                  v
                +------------------+
                | Display Response |
                +------------------+
                          |
                          v
                         End
```
