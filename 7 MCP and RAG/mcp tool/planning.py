import json
from anthropic import Anthropic
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters
)
from mcp import ClientSession


# ============================================================
# CLAUDE CLIENT
# ============================================================

client = Anthropic(
    api_key=""
)


# ============================================================
# MAIN PLANNER LOGIC
# ============================================================

async def run_flight_planner():

    # Get user details
    name = input("Passenger Name : ")
    source = input("Source City    : ")
    destination = input("Destination    : ")
    date = input("Travel Date    : ")


    # Natural language query
    query = f"""
    Book a flight for {name}
    from {source}
    to {destination}
    on {date}
    """


    # MCP server configuration
    server_params = StdioServerParameters(

        command="python",
        args=["mcp_server.py"]

    )


    # Connect to MCP server
    async with stdio_client(
        server_params
    ) as (

        read_stream,
        write_stream

    ):


        async with ClientSession(

            read_stream,
            write_stream

        ) as session:


            # Initialize server connection
            await session.initialize()


            # Get all available tools
            tools = await session.list_tools()


            print(
                "\n========== GENERATED TOOL SCHEMAS =========="
            )


            anthropic_tools = []


            # Build Claude tool schemas
            for tool in tools.tools:

                print(
                    "\nTool Name:",
                    tool.name
                )


                print(

                    json.dumps(
                        tool.inputSchema,
                        indent=4
                    )
                )


                anthropic_tools.append(

                    {

                        "name":
                        tool.name,

                        "description":
                        tool.description,

                        "input_schema":
                        tool.inputSchema

                    }

                )


            # Send request to Claude
            response = client.messages.create(

                model=
                "claude-sonnet-4-20250514",

                max_tokens=
                1000,

                tools=
                anthropic_tools,

                messages=[

                    {

                        "role":
                        "user",

                        "content":
                        query

                    }

                ]

            )


            # Process tool calls
            for item in response.content:


                if item.type == "tool_use":

                    print(
                        "\n========== TOOL CALLED =========="
                    )

                    print(
                        "Tool Name:",
                        item.name
                    )

                    print(
                        "Arguments:",
                        item.input
                    )


                    # Execute tool
                    result = await session.call_tool(

                        item.name,
                        item.input

                    )


                    # Flight planning result
                    if item.name == "planning_tool":


                        flight_data = json.loads(

                            result.content[0].text

                        )


                        print(
                            "\n========== FLIGHT DETAILS =========="
                        )


                        print(f"""
Flight Number : {flight_data["flight_number"]}
Source        : {flight_data["source"]}
Destination   : {flight_data["destination"]}
Date          : {flight_data["date"]}
Price         : {flight_data["price"]}
Status        : {flight_data["status"]}
""")


                        print(
                            "\n========== TOOL CALLED =========="
                        )

                        print(
                            "Tool Name : notification_tool"
                        )


                        # Send notification
                        notification_result = (

                            await session.call_tool(

                                "notification_tool",

                                {

                                    "user_name":
                                    name,

                                    "flight_number":
                                    flight_data[
                                        "flight_number"
                                    ]

                                }

                            )

                        )


                        print(
                            "\n====== BOOKING CONFIRMATION ======"
                        )


                        print(

                            notification_result
                            .content[0]
                            .text

                        )