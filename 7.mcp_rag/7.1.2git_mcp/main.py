import asyncio
import os

# Load environment variables from the .env file
from dotenv import load_dotenv

# MCP classes used to connect to an MCP server
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables (e.g., GitHub token)
load_dotenv()


async def main():

    # Configure how to start the GitHub MCP Server
    server = StdioServerParameters(

        # Run the server using npx
        command="npx",

        # Download (if needed) and start the official GitHub MCP server
        args=["-y", "@modelcontextprotocol/server-github"],

        # Pass the GitHub Personal Access Token to the server
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
        },
    )

    # Start the GitHub MCP server and establish communication
    async with stdio_client(server) as (read, write):

        # Create an MCP client session using the communication channels
        async with ClientSession(read, write) as session:

            # Initialize the connection with the MCP server
            await session.initialize()

            # Request all tools that the GitHub MCP server provides
            tools = await session.list_tools()

            print("Available GitHub Tools:\n")

            # Loop through each tool returned by the server
            for tool in tools.tools:

                # Print the tool's name
                print(f"Name: {tool.name}")

                # Print a short description of what the tool does
                print(f"Description: {tool.description}")

                print("-" * 50)


# Start the async program
asyncio.run(main())