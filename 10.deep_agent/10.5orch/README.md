# Setup
User Input: You type: "I want to book a flight from Bangalore to Delhi."
Orchestrator Decision: The Orchestrator agent recognizes you want to travel and calls the planning_agent tool first to parse your query.
Extraction: The planning_agent tool parses your text to extract:
source: "Bangalore"
destination: "Delhi"
Orchestrator Decision: Armed with the parsed source and destination, the Orchestrator proceeds directly to call search_worker(source="Bangalore", destination="Delhi").

Flight Search
Search Execution: The search_worker matches the route against a list of flights and returns a random flight option (e.g. FL101, 6:30 PM, ₹5200).
Agent Response: The Orchestrator shows you the flight details and asks if you would like to proceed with the booking.

Interactive Booking Worker (Form Collection)
User Input: You type: "Yes, proceed."
Orchestrator Decision: The Orchestrator calls the booking_worker tool.
Worker Execution: The booking_worker runs interactively in the terminal console, prompting you for input step-by-step:
Prompts for passenger Name (e.g., "John Doe").
Prompts for passenger Phone (e.g., "1234567").
Displays a seat map (A1-C3) and prompts for a Seat choice (e.g., "A1").
Prompts for payment execution (asks you to type "pay").
Booking Output: If payment is successful, the worker returns a dictionary confirming the booking details and status "CONFIRMED".

Final Notification
Orchestrator Decision: Upon receiving the successful status from the booking worker, the Orchestrator formats the booking data and passes it to the final worker tool, notification_worker.
Receipt Output: The notification_worker returns a formatted final booking confirmation card:
text
BOOKING CONFIRMED
Details: [Passenger Info, Route, Seat]
Payment Successful
Have a safe journey.
Agent Response: The Orchestrator presents this receipt to you in the chat console to finish the workflow.

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
                | Orchestrator     |
                | Receives query   |
                +------------------+
                          |
                          v
                +------------------+
                | Delegates tasks  |
                | to sub-workers   |
                +------------------+
                     /     |     \
            Search Worker  |    Notification Worker
                 /   Booking Worker   \
                v          v           v
        +---------+   +---------+   +---------+
        | Search  |   | Booking |   | Notify  |
        +---------+   +---------+   +---------+
                 \         |         /
                  v        v        v
                +------------------+
                | Orchestrator     |
                | compiles results |
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
