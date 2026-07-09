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
                |    StateGraph    |
                +------------------+
                          |
                          v
                +------------------+
                |  generate_plan   |
                | LLM parses steps |
                |  into JSON list  |
                +------------------+
                          |
                          v
                +------------------+
                | Loop through JSON|
                | Steps in State   |
                +------------------+
                          |
                          v
                +------------------+
                | Execute Step Tool|
                | Search/Book/Fare |
                | /Price/Cancel    |
                +------------------+
                          |
                          v
                +------------------+
                |generate_response |
                | Build final text |
                | summary using state|
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
