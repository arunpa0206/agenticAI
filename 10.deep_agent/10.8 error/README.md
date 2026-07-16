# Setup

1. Install dependencies

pip install -r requirements.txt


2. Add your API key

Open the project files and replace:

api_key="YOUR_API_KEY"

with your own Anthropic API key.


3. Activate Virtual Environment (PowerShell)

Depending on your current working directory in the terminal, run:
* **From the project root (`o:\training_arun\10.deep_agent\10.8 error`):**
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
Search Flight Execution & Simulation Failure
User Input: You type: "Show me flights from Bangalore to Delhi."
Agent Decision: The agent invokes the search_flight tool.
Error Trigger: Inside the tool, the program checks current_time % 2 == 0 (even seconds) to simulate a random system connection crash:
If Time is Odd (No Error): The tool proceeds directly to generate flight options (Air India, Indigo, etc.) and presents them.
If Time is Even (Error Occurs): The tool raises an exception: "Flight search system failure".

Execution of the Error Handler (error_handler.py)
If the search fails, execution jumps to the except Exception block, which calls handle_error() from 
error_handler.py
.
The error handler:
Outputs [ERROR HANDLER] on the console.
Sleeps for 2 seconds (time.sleep(2)) to allow connection buffers to clear.
Checks time.time() % 2 != 0 (whether the current time is odd after the sleep) to test recovery success:
Success Route (Odd time): Prints "Recovered", returns {"status": "success"}, and the tool continues to search and successfully returns flight results.
Failure Route (Even time): Prints "Retry failed", returns {"status": "error"}, triggers failure_notification(), and returns "Search unavailable".

Booking & Confirmation
If Search Recovered:
The user selects a flight.
The agent calls the booking_agent to ask for the passenger's name.
The agent calls the success_notification tool to output a success booking card to complete the workflow.
If Search Failed Completely:
The agent calls failure_notification to output a failure error screen.
The agent returns "Search unavailable." and exits the workflow.

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
                | Execute Agent    |
                +------------------+
                          |
                          v
                +------------------+
                | Error Handler    |
                | Intercepts error |
                +------------------+
                     /            \
               Recovered        Failed
                  /                \
                 v                  v
        +------------------+   +------------------+
        | Retry / Alternate|   | Notify Failure   |
        | task execution   |   | & Log details    |
        +------------------+   +------------------+
                  \                 /
                   v               v
                +------------------+
                | Display Response |
                +------------------+
                          |
                          v
                         End
```
