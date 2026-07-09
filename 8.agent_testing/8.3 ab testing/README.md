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
                | test_ab_testing  |
                +------------------+
                          |
                          v
                +------------------+
                | Run 100 loops    |
                | Executing Agent A|
                | & Agent B        |
                +------------------+
                          |
                          v
                +------------------+
                | Collect metrics  |
                | Success, steps,  |
                | tool accuracy    |
                +------------------+
                          |
                          v
                +------------------+
                | Compare Results  |
                | Print Win Rate   |
                | & comparison     |
                +------------------+
                          |
                          v
                         End
```
