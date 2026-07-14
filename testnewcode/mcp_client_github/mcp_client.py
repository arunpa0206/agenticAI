import sys
import asyncio
import os

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Reconfigure stdout to support UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()


# ------------------------------------
# 1. Create Session
# ------------------------------------
async def create_session():
    """
    Starts the GitHub MCP server and creates a client session.
    """

    server = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN":
                os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
        },
    )

    stdio = stdio_client(server)
    read, write = await stdio.__aenter__()

    session = ClientSession(read, write)
    await session.__aenter__()

    await session.initialize()

    return session, stdio


# ------------------------------------
# 2. List Tools
# ------------------------------------
async def list_tools(session):
    """
    Lists all tools exposed by the GitHub MCP server.
    """

    tools = await session.list_tools()

    print("\nAvailable Tools:\n")

    for tool in tools.tools:
        print(f"Tool Name : {tool.name}")
        print(f"Description : {tool.description}")
        print("-" * 50)


# ------------------------------------
# 3. Invoke Tool
# ------------------------------------
async def invoke_tool(session):
    """
    Invokes the search_repositories tool.
    """

    result = await session.call_tool(
        "search_repositories",
        {
            "query": "python",
            "page": 1
        }
    )

    print("\nSearch Repository Result:\n")
    print(result.content)


# ------------------------------------
# 4. Main
# ------------------------------------
async def main():

    # Create a session
    session, stdio = await create_session()

    # List all available tools
    await list_tools(session)

    # Invoke the search_repositories tool
    await invoke_tool(session)

    # Cleanup
    await session.__aexit__(None, None, None)
    await stdio.__aexit__(None, None, None)


if __name__ == "__main__":
    asyncio.run(main())