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
                |  Initialize Graph|
                |   LangGraph with |
                |   LangChain Tools|
                +------------------+
                          |
                          v
                +------------------+
                |  Planning Node   |
                | LLM plans booking|
                | steps list       |
                +------------------+
                          |
                          v
                +------------------+
                |   Action Node    |
                | Execute LangChain|
                | tools in sequence|
                +------------------+
                          |
                          v
                +------------------+
                |  Response Node   |
                | Formulate final  |
                | customer summary |
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
