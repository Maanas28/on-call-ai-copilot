import json

from app.service import (
    list_open_incidents,
    get_incident_details,
    acknowledge_incident,
    assign_to_engineer,
    add_resolution_note,
    resolve_incident,
)

from llm_agent.trace_logger import log_step


def execute_tool(tool_name: str, arguments):
    if isinstance(arguments, str):
        arguments = json.loads(arguments or "{}")

    log_step(
        "5. DISPATCHER ROUTING",
        "Dispatcher is mapping the selected tool to the correct service function.",
        {
            "tool_name": tool_name,
            "arguments": arguments
        }
    )

    if tool_name == "list_open_incidents_tool":
        log_step(
            "6. SERVICE LAYER CALL",
            "Calling service.list_open_incidents()."
        )
        return list_open_incidents()

    if tool_name == "get_incident_details_tool":
        log_step(
            "6. SERVICE LAYER CALL",
            "Calling service.get_incident_details(incident_id).",
            {
                "incident_id": arguments["incident_id"]
            }
        )
        return get_incident_details(arguments["incident_id"])

    if tool_name == "acknowledge_incident_tool":
        log_step(
            "6. SERVICE LAYER CALL",
            "Calling service.acknowledge_incident(incident_id).",
            {
                "incident_id": arguments["incident_id"]
            }
        )
        return acknowledge_incident(arguments["incident_id"])

    if tool_name == "assign_to_engineer_tool":
        log_step(
            "6. SERVICE LAYER CALL",
            "Calling service.assign_to_engineer(incident_id, engineer_id).",
            {
                "incident_id": arguments["incident_id"],
                "engineer_id": arguments["engineer_id"]
            }
        )
        return assign_to_engineer(
            arguments["incident_id"],
            arguments["engineer_id"],
        )

    if tool_name == "add_resolution_note_tool":
        log_step(
            "6. SERVICE LAYER CALL",
            "Calling service.add_resolution_note(incident_id, note).",
            {
                "incident_id": arguments["incident_id"],
                "note": arguments["note"]
            }
        )
        return add_resolution_note(
            arguments["incident_id"],
            arguments["note"],
        )

    if tool_name == "resolve_incident_tool":
        log_step(
            "6. SERVICE LAYER CALL",
            "Calling service.resolve_incident(incident_id).",
            {
                "incident_id": arguments["incident_id"]
            }
        )
        return resolve_incident(arguments["incident_id"])

    raise ValueError(f"Unknown tool: {tool_name}")