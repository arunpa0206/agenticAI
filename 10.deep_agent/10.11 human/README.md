# Setup

1. Install dependencies

pip install -r requirements.txt


2. Add your API key

Open the project files and replace:

api_key="YOUR_API_KEY"

with your own Anthropic API key.


3. Run the project

python main.py

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
