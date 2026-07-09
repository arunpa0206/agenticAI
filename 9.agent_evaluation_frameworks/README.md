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
                | Load prompts &   |
                | golden datasets  |
                +------------------+
                          |
                          v
                +------------------+
                | Loop through 114 |
                | test prompts     |
                +------------------+
                          |
                          v
                +------------------+
                | Get LLM Response |
                | from Chatbot     |
                +------------------+
                          |
                          v
                +------------------+
                | evaluate_metrics |
                | Match expected   |
                | tools & output   |
                +------------------+
                          |
                          v
                +------------------+
                | generate_output  |
                | Save results to  |
                | output.json      |
                +------------------+
                          |
                          v
                +------------------+
                | Print "Done"     |
                +------------------+
                          |
                          v
                         End
```
