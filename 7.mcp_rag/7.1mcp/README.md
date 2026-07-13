# Run Instructions

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your API Key

Open `planning.py` and replace:

```python
api_key="YOUR_API_KEY"
```

with your own Anthropic API key.

Alternatively, create a `.env` file:

```text
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Run the project

```bash
python main.py
```

---

# Code Execution Flow

```text
                    +------------------+
                    |   Start Program  |
                    |    python main.py|
                    +------------------+
                              |
                              v
                    +------------------+
                    |  Start MCP Server|
                    | (stdio transport)|
                    +------------------+
                              |
                              v
                    +------------------+
                    | User Enters Query|
                    +------------------+
                              |
                              v
                    +------------------+
                    | Client Connects  |
                    | to MCP Server    |
                    +------------------+
                              |
                              v
                    +------------------+
                    | Discover Tools   |
                    | session.list_tools()|
                    +------------------+
                              |
                              v
                    +------------------+
                    | Claude Chooses   |
                    | Appropriate Tool |
                    +------------------+
                              |
                              v
                    +------------------+
                    | Execute Tool     |
                    | session.call_tool()|
                    +------------------+
                              |
                              v
                    +------------------+
                    | MCP Server Runs  |
                    | hello_tool() /   |
                    | add_tool()       |
                    +------------------+
                              |
                              v
                    +------------------+
                    | Return Result    |
                    | to Client        |
                    +------------------+
                              |
                              v
                    +------------------+
                    | Display Output   |
                    +------------------+
                              |
                              v
                             End
```

## Project Flow

1. The client starts and launches the MCP server.
2. The client establishes an MCP session.
3. Available tools are discovered using `list_tools()`.
4. The user's query is sent to Claude.
5. Claude decides which MCP tool should be used.
6. The client invokes the selected tool using `call_tool()`.
7. The MCP server executes the tool and returns the result.
8. The client displays the tool's response.

This project demonstrates the complete MCP workflow:
- Creating an MCP server
- Registering tools
- Discovering available tools
- Allowing an LLM to choose a tool
- Executing the tool through the MCP protocol
- Returning the result to the user