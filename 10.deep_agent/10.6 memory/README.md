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
