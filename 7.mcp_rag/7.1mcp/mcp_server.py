from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DemoServer")


@mcp.tool()
def hello_tool(name: str):
    """Greets the user."""
    return f"Hello {name}! Welcome to MCP."


@mcp.tool()
def add_tool(a: int, b: int):
    """Adds two numbers."""
    return a + b


if __name__ == "__main__":
    mcp.run()