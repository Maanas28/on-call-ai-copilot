INCIDENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_open_incidents_tool",
            "description": "List all currently open incidents.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_incident_details_tool",
            "description": "Get details for a specific incident.",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "string",
                        "description": "Incident ID, for example INC-1001"
                    }
                },
                "required": ["incident_id"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "acknowledge_incident_tool",
            "description": "Acknowledge an incident.",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "string",
                        "description": "Incident ID, for example INC-1001"
                    }
                },
                "required": ["incident_id"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "assign_to_engineer_tool",
            "description": "Assign an incident to an engineer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "string"
                    },
                    "engineer_id": {
                        "type": "string"
                    }
                },
                "required": ["incident_id", "engineer_id"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_resolution_note_tool",
            "description": "Add an investigation or resolution note to an incident.",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "string"
                    },
                    "note": {
                        "type": "string"
                    }
                },
                "required": ["incident_id", "note"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "resolve_incident_tool",
            "description": "Resolve an incident.",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "string"
                    }
                },
                "required": ["incident_id"]
            },
        },
    },
]