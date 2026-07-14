import json
import os
from dotenv import load_dotenv

from anthropic import Anthropic
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


async def run_demo():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            anthropic_tools = []

            for tool in tools.tools:
                anthropic_tools.append(
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema,
                    }
                )

            print("\nType 'exit' or 'quit' to end the demo.\n")

            while True:

                query = input("Enter your query: ")

                if query.lower() in ["exit", "quit"]:
                    print("\nExiting MCP Demo...")
                    break

                response = client.messages.create(
                    model="claude-sonnet-5",
                    max_tokens=300,
                    tools=anthropic_tools,
                    messages=[
                        {
                            "role": "user",
                            "content": query,
                        }
                    ],
                )

                tool_used = False

                for item in response.content:

                    if item.type == "tool_use":

                        tool_used = True

                        print("\nTool Selected :", item.name)
                        print("Arguments     :", item.input)

                        result = await session.call_tool(
                            item.name,
                            item.input,
                        )

                        print("\nTool Result:")
                        print(result.content[0].text)

                if not tool_used:

                    print("\nClaude's Response:")

                    for item in response.content:

                        if item.type == "text":
                            print(item.text)

                print()