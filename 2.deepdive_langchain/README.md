# Setup

1. Install dependencies

pip install -r requirements.txt


2. Add your API key

Open the project files and replace:

api_key="YOUR_API_KEY"

with your own API key.


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
                |   LangChain Agent|
                | Bind Tools to    |
                | ChatAnthropic    |
                +------------------+
                          |
                          v
                +------------------+
                |  ChatAnthropic   |
                | Decides Tool or  |
                | Response Output  |
                +------------------+
                     /        \
         Tool Selected        Final Text Answer
                   /            \
                  v              v
        +------------------+   +------------------+
        |   Execute Tool   |   | Display Response |
        | Search/Book/etc. |   +------------------+
        +------------------+             |
                  |                      v
                  v                     End
        Pass Tool Result
        Back to Model
                  |
                  v
        (Loop back to decision)
```
