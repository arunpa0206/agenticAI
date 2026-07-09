# Setup

1. Install dependencies

pip install -r requirements.txt


2. Run the project

python main.py

---

## Code Execution Flow

```text
                +------------------+
                |    Start Program |
                +------------------+
                          |
                          v
                +------------------+
                | User Enters Query|
                +------------------+
                          |
                          v
                +------------------+
                |    AI Agent       |
                | Build Prompt &    |
                | Send to Claude    |
                +------------------+
                          |
                          v
                +------------------+
                | Claude Decides   |
                | SEARCH / BOOK /  |
                | CANCEL / ANOTHER |
                +------------------+
                          |
                          v
                +------------------+
                | Execute Function |
                | Search / Book /  |
                | Cancel Flight    |
                +------------------+
                          |
                          v
                +------------------+
                | Display Response |
                +------------------+
                          |
                          v
                +------------------+
                | Another Query?   |
                +------------------+
                     |         |
                   Yes         No
                     |         |
                     v         v
             Back to User     End
```