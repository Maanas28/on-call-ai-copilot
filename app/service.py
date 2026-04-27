from dataclasses import asdict

from app.store import INCIDENTS, ENGINEERS
from llm_agent.trace_logger import log_step

def list_open_incidents():
    log_step(
        "SERVICE BUSINESS LOGIC",
        "Inside service layer: listing all open incidents."
    )

    open_incidents = [
        asdict(incident)
        for incident in INCIDENTS
        if incident.status == "OPEN"
    ]

    log_step(
        "MOCK STORE RESULT",
        "Fetched open incidents from in-memory mock store.",
        {
            "open_incident_count": len(open_incidents),
            "open_incidents": open_incidents,
        }
    )

    return open_incidents

def get_incident_details(incident_id: str):
    log_step(
        "SERVICE BUSINESS LOGIC",
        "Inside service layer: fetching incident details.",
        {
            "incident_id": incident_id
        }
    )

    for incident in INCIDENTS:
        if incident.id == incident_id:
            incident_data = asdict(incident)

            log_step(
                "MOCK STORE RESULT",
                "Incident found in in-memory mock store.",
                {
                    "incident": incident_data
                }
            )

            return incident_data

    log_step(
        "SERVICE ERROR",
        "Incident was not found in the in-memory mock store.",
        {
            "incident_id": incident_id
        }
    )

    raise ValueError(f"Incident {incident_id} not found")

def acknowledge_incident(incident_id: str):
    log_step(
        "SERVICE BUSINESS LOGIC",
        "Inside service layer: acknowledging incident.",
        {
            "incident_id": incident_id
        }
    )

    for incident in INCIDENTS:
        if incident.id == incident_id:
            if incident.status == "RESOLVED":
                log_step(
                    "SERVICE VALIDATION FAILED",
                    "Resolved incident cannot be acknowledged.",
                    {
                        "incident_id": incident_id,
                        "current_status": incident.status,
                    }
                )

                raise ValueError("Resolved incident cannot be acknowledged")

            old_status = incident.status
            incident.status = "ACKNOWLEDGED"

            incident_data = asdict(incident)

            log_step(
                "MOCK STORE UPDATED",
                "Incident status updated in in-memory mock store.",
                {
                    "incident_id": incident_id,
                    "old_status": old_status,
                    "new_status": incident.status,
                    "incident": incident_data,
                }
            )

            return {
                "message": f"Incident {incident_id} acknowledged successfully",
                "incident": incident_data,
            }

    log_step(
        "SERVICE ERROR",
        "Incident was not found in the in-memory mock store.",
        {
            "incident_id": incident_id
        }
    )

    raise ValueError(f"Incident {incident_id} not found")


def assign_to_engineer(incident_id: str, engineer_id: str):
    log_step(
        "SERVICE BUSINESS LOGIC",
        "Inside service layer: assigning incident to engineer.",
        {
            "incident_id": incident_id,
            "engineer_id": engineer_id,
        }
    )

    engineer = None

    for eng in ENGINEERS:
        if eng.id == engineer_id:
            engineer = eng
            break

    if engineer is None:
        log_step(
            "SERVICE VALIDATION FAILED",
            "Engineer was not found in the in-memory mock store.",
            {
                "engineer_id": engineer_id
            }
        )

        raise ValueError(f"Engineer {engineer_id} not found")

    log_step(
        "MOCK STORE RESULT",
        "Engineer found in in-memory mock store.",
        {
            "engineer": asdict(engineer)
        }
    )

    for incident in INCIDENTS:
        if incident.id == incident_id:
            old_assigned_to = incident.assigned_to
            incident.assigned_to = engineer.name

            incident_data = asdict(incident)

            log_step(
                "MOCK STORE UPDATED",
                "Incident assignment updated in in-memory mock store.",
                {
                    "incident_id": incident_id,
                    "old_assigned_to": old_assigned_to,
                    "new_assigned_to": incident.assigned_to,
                    "incident": incident_data,
                }
            )

            return {
                "message": f"Incident {incident_id} assigned to {engineer.name}",
                "incident": incident_data,
            }

    log_step(
        "SERVICE ERROR",
        "Incident was not found in the in-memory mock store.",
        {
            "incident_id": incident_id
        }
    )

    raise ValueError(f"Incident {incident_id} not found")


def add_resolution_note(incident_id: str, note: str):
    log_step(
        "SERVICE BUSINESS LOGIC",
        "Inside service layer: adding note to incident.",
        {
            "incident_id": incident_id,
            "note": note,
        }
    )

    for incident in INCIDENTS:
        if incident.id == incident_id:
            old_note_count = len(incident.notes)

            incident.notes.append(note)

            incident_data = asdict(incident)

            log_step(
                "MOCK STORE UPDATED",
                "Incident note added in in-memory mock store.",
                {
                    "incident_id": incident_id,
                    "old_note_count": old_note_count,
                    "new_note_count": len(incident.notes),
                    "incident": incident_data,
                }
            )

            return {
                "message": f"Note added to incident {incident_id}",
                "incident": incident_data,
            }

    log_step(
        "SERVICE ERROR",
        "Incident was not found in the in-memory mock store.",
        {
            "incident_id": incident_id
        }
    )

    raise ValueError(f"Incident {incident_id} not found")


def resolve_incident(incident_id: str):
    log_step(
        "SERVICE BUSINESS LOGIC",
        "Inside service layer: resolving incident.",
        {
            "incident_id": incident_id
        }
    )

    for incident in INCIDENTS:
        if incident.id == incident_id:
            old_status = incident.status
            incident.status = "RESOLVED"

            incident_data = asdict(incident)

            log_step(
                "MOCK STORE UPDATED",
                "Incident status updated to RESOLVED in in-memory mock store.",
                {
                    "incident_id": incident_id,
                    "old_status": old_status,
                    "new_status": incident.status,
                    "incident": incident_data,
                }
            )

            return {
                "message": f"Incident {incident_id} resolved successfully",
                "incident": incident_data,
            }

    log_step(
        "SERVICE ERROR",
        "Incident was not found in the in-memory mock store.",
        {
            "incident_id": incident_id
        }
    )

    raise ValueError(f"Incident {incident_id} not found")