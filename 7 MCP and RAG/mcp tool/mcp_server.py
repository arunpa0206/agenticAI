from mcp.server.fastmcp import FastMCP
from notification import send_confirmation


mcp = FastMCP(
    "FlightPlanner"
)


@mcp.tool()
def planning_tool(
    source:str,
    destination:str,
    date:str
):

    return {

        "flight_number":"AI-203",
        "source":source,
        "destination":destination,
        "date":date,
        "price":"₹7500",
        "status":"Available"

    }


@mcp.tool()
def notification_tool(
    user_name:str,
    flight_number:str
):

    return send_confirmation(

        user_name,
        flight_number

    )


if __name__=="__main__":

    mcp.run()