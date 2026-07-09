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
                | test_integration |
                +------------------+
                          |
                          v
                +------------------+
                | Execute Flow     |
                | plan -> select ->|
                | confirm -> cancel|
                +------------------+
                          |
                          v
                +------------------+
                | Assert relevance |
                | Check consistency|
                | of responses     |
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
