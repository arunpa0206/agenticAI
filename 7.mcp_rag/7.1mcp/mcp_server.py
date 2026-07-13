from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DemoServer")


@mcp.tool()
def add(a: int, b: int):
    """Add two numbers."""
    return a + b


@mcp.tool()
def subtract(a: int, b: int):
    """Subtract two numbers."""
    return a - b


if __name__ == "__main__":
    mcp.run()