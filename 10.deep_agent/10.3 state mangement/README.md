# Setup
Step 1: Flight Search

The user asks to see flights.
The agent calls the generate_flight_plan() tool.
The tool picks a random flight, reads state.json via load_state(), writes the flight information, resets all other details to defaults, sets the progress step to FLIGHT_GENERATED, and writes back to state.json via save_state().
The agent presents the flight to the user and asks for passenger details.

Step 2: Passenger Details

The user provides their name and phone number.
The agent calls the booking_workflow() tool.
The tool reads state.json, saves the passenger details, sets the booking status to BOOKED, sets the progress step to CUSTOMER_DETAILS_ADDED, and saves the state.
The agent asks the user to confirm the payment.
\
Step 3: Payment Processing

The user confirms payment.
The agent calls the payment_workflow(payment_confirmed=True) tool.
The tool reads state.json, marks the payment status as PAID, sets the progress step to PAYMENT_COMPLETED, and saves the state.
The agent moves to final verification.

Step 4: Final Confirmation

The agent calls the notification_workflow() tool.
The tool reads all of the accumulated details (flight route, customer name, booking status, and payment status) from state.json and formats them into a final confirmation receipt card.
The agent displays this confirmation receipt card to the user.

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
                | Load State       |
                | Read state.json  |
                +------------------+
                          |
                          v
                +------------------+
                | User Enters Query|
                +------------------+
                          |
                          v
                +------------------+
                |   Agent Execution|
                | Runs planning,   |
                | updating state   |
                +------------------+
                          |
                          v
                +------------------+
                | Save State       |
                | Write state.json |
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
