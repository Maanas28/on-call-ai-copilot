from dataclasses import asdict
from app.store import INCIDENTS, ENGINEERS

def list_open_incidents():
    return [asdict(incident) for incident in INCIDENTS if incident.status == "OPEN"]


def get_incident_details(incident_id: str):
    for incident in INCIDENTS:
        if incident.id == incident_id:
            return asdict(incident)
    raise ValueError(f"Incident {incident_id} not found")

def acknowledge_incident(incident_id: str):
    for incident in INCIDENTS:
        if incident.id == incident_id:
            if incident.status == "RESOLVED":
                raise ValueError("Resolved incident cannot be acknowledged")
            incident.status = "ACKNOWLEDGED"
            return {
                "message": f"Incident {incident_id} acknowledged successfully",
                "incident": asdict(incident),
            }
    raise ValueError(f"Incident {incident_id} not found")

def assign_to_engineer(incident_id: str, engineer_id: str):
    engineer = None
    for eng in ENGINEERS:
        if eng.id == engineer_id:
            engineer = eng
            break

    if engineer is None:
        raise ValueError(f"Engineer {engineer_id} not found")

    for incident in INCIDENTS:
        if incident.id == incident_id:
            incident.assigned_to = engineer.name
            return {
                "message": f"Incident {incident_id} assigned to {engineer.name}",
                "incident": asdict(incident),
            }

    raise ValueError(f"Incident {incident_id} not found")

def add_resolution_note(incident_id: str, note: str):
    for incident in INCIDENTS:
        if incident.id == incident_id:
            incident.notes.append(note)
            return {
                "message": f"Note added to incident {incident_id}",
                "incident": asdict(incident),
            }
    raise ValueError(f"Incident {incident_id} not found")

def resolve_incident(incident_id: str):
    for incident in INCIDENTS:
        if incident.id == incident_id:
            incident.status = "RESOLVED"
            return {
                "message": f"Incident {incident_id} resolved successfully",
                "incident": asdict(incident),
            }
    raise ValueError(f"Incident {incident_id} not found")

