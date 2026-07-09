How to Run the Program

# Setup

1. Install dependencies

pip install -r requirements.txt


2. Add your API key

Open the project files and replace:

anthropic_api_key="YOUR_API_KEY"

with your own Anthropic API key.


3. Run the project

python main.py

---

## Code Execution Flow

```text
                +------------------+
                |  Start Testing   |
                +------------------+
                          |
                          v
                +------------------+
                | Run unittest     |
                | test_flight_booking|
                +------------------+
                          |
                          v
                +------------------+
                |  Test Cases      |
                | Mock & test      |
                | tools/functions  |
                +------------------+
                          |
                          v
                +------------------+
                | Assert Behaviors |
                | Check return     |
                | matches expected |
                +------------------+
                          |
                          v
                +------------------+
                | Print Result     |
                | OK / FAILED      |
                +------------------+
                          |
                          v
                         End
```
