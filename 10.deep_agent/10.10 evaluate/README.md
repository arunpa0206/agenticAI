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
                | Run Deep Agent   |
                +------------------+
                          |
                          v
                +------------------+
                | Evaluate output  |
                | against expected |
                +------------------+
                          |
                          v
                +------------------+
                | Output Evaluation|
                | Metrics / result |
                +------------------+
                          |
                          v
                         End
```
