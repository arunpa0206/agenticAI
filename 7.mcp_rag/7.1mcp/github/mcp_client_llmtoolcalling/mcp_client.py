import sys
import asyncio
import os

from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Reconfigure stdout to support UTF-8 on Windows
sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables
load_dotenv()

# Anthropic client
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


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

    # Start the GitHub MCP server
    stdio = stdio_client(server)
    read, write = await stdio.__aenter__()

    # Create a client session
    session = ClientSession(read, write)
    await session.__aenter__()

    # Initialize the session
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

    print("\nAvailable GitHub Tools:\n")

    for tool in tools.tools:
        print(f"Tool Name   : {tool.name}")
        print(f"Description : {tool.description}")
        print("-" * 60)


# ------------------------------------
# 3. LLM Tool Calling
# ------------------------------------
async def llm_tool_calling(session):
    """
    Lets Claude choose and invoke one of the GitHub MCP tools in a loop.
    """

    # Get all GitHub tools once at startup
    tools = await session.list_tools()
    anthropic_tools = []

    # Convert MCP tools into Anthropic tool format
    for tool in tools.tools:
        anthropic_tools.append(
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
        )

    print("\nType 'exit' or 'quit' to end the session.\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            print("\nExiting session...")
            break

        if not query.strip():
            continue

        # Send the user query and tools to Claude
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": query,
                }
            ],
            tools=anthropic_tools,
        )

        tool_called = False

        # Check whether Claude selected a tool
        for block in response.content:

            if block.type == "tool_use":

                tool_called = True

                print(f"\nClaude selected tool: {block.name}")
                print(f"Arguments: {block.input}")

                # Invoke the selected MCP tool
                result = await session.call_tool(
                    block.name,
                    block.input,
                )

                print("\nTool Result:\n")
                print(result.content)

        if not tool_called:

            print("\nClaude did not select a tool.")
            text_response = "".join([block.text for block in response.content if block.type == "text"])
            print(text_response)

        print()


# ------------------------------------
# 4. Main
# ------------------------------------
async def main():

    # Create a session with the GitHub MCP server
    session, stdio = await create_session()

    # Display all available GitHub tools
    await list_tools(session)

    # Allow Claude to select and invoke one of the tools
    await llm_tool_calling(session)

    # Close the session and stop the server
    await session.__aexit__(None, None, None)
    await stdio.__aexit__(None, None, None)


if __name__ == "__main__":
    asyncio.run(main())