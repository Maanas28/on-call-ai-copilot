from mcp.server.fastmcp import FastMCP

from app.service import (
    list_open_incidents,
    get_incident_details,
    acknowledge_incident,
    assign_to_engineer,
    add_resolution_note,
    resolve_incident,
)

mcp = FastMCP("OnCall Demo MCP")


@mcp.tool()
def list_open_incidents_tool() -> list[dict]:
    """Return all currently open incidents."""
    return list_open_incidents()


@mcp.tool()
def get_incident_details_tool(incident_id: str) -> dict:
    """Return full details for a single incident."""
    return get_incident_details(incident_id)


@mcp.tool()
def acknowledge_incident_tool(incident_id: str) -> dict:
    """Acknowledge an open incident."""
    return acknowledge_incident(incident_id)


@mcp.tool()
def assign_to_engineer_tool(incident_id: str, engineer_id: str) -> dict:
    """Assign an incident to an engineer."""
    return assign_to_engineer(incident_id, engineer_id)


@mcp.tool()
def add_resolution_note_tool(incident_id: str, note: str) -> dict:
    """Add a resolution or investigation note to an incident."""
    return add_resolution_note(incident_id, note)


@mcp.tool()
def resolve_incident_tool(incident_id: str) -> dict:
    """Mark an incident as resolved."""
    return resolve_incident(incident_id)


if __name__ == "__main__":
    print("Starting OnCall Demo MCP server...")
    mcp.run(transport="stdio")