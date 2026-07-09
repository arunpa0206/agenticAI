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
