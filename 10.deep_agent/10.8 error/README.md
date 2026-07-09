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
                | Execute Agent    |
                +------------------+
                          |
                          v
                +------------------+
                | Error Handler    |
                | Intercepts error |
                +------------------+
                     /            \
               Recovered        Failed
                  /                \
                 v                  v
        +------------------+   +------------------+
        | Retry / Alternate|   | Notify Failure   |
        | task execution   |   | & Log details    |
        +------------------+   +------------------+
                  \                 /
                   v               v
                +------------------+
                | Display Response |
                +------------------+
                          |
                          v
                         End
```
