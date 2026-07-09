Run Instructions
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
                |   Start Servers  |
                |  Run MCP Server  |
                +------------------+
                          |
                          v
                +------------------+
                | Client Runs Code |
                | User Enters Query|
                +------------------+
                          |
                          v
                +------------------+
                |  Planner Agent   |
                | Sends requests   |
                | to MCP Server    |
                +------------------+
                          |
                          v
                +------------------+
                |  MCP Server      |
                | Executes search /|
                | booking tool     |
                +------------------+
                          |
                          v
                +------------------+
                |  Notify Agent    |
                | Send email/sms   |
                | notification     |
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
