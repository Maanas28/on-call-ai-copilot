import json
from app.service import (
    list_open_incidents,
    get_incident_details,
    acknowledge_incident,
    assign_to_engineer,
    add_resolution_note,
    resolve_incident,
)


def run_agent(user_message: str):
    message = user_message.lower()

    if "open incident" in message or "list incident" in message:
        return list_open_incidents()

    if "details" in message:
        incident_id = extract_incident_id(user_message)
        return get_incident_details(incident_id)

    if "acknowledge" in message or "ack" in message:
        incident_id = extract_incident_id(user_message)
        return acknowledge_incident(incident_id)

    if "assign" in message:
        incident_id = extract_incident_id(user_message)
        engineer_id = extract_engineer_id(user_message)
        return assign_to_engineer(incident_id, engineer_id)

    if "note" in message:
        incident_id = extract_incident_id(user_message)
        note = user_message
        return add_resolution_note(incident_id, note)

    if "resolve" in message:
        incident_id = extract_incident_id(user_message)
        return resolve_incident(incident_id)

    return {
        "message": "Sorry, I could not understand which tool to call."
    }


def extract_incident_id(text: str):
    words = text.split()

    for word in words:
        cleaned = word.upper().replace(",", "").replace(".", "")
        if cleaned.startswith("INC"):
            return cleaned

    raise ValueError("Incident id not found in message")


def extract_engineer_id(text: str):
    words = text.split()

    for word in words:
        cleaned = word.upper().replace(",", "").replace(".", "")
        if cleaned.startswith("ENG"):
            return cleaned

    raise ValueError("Engineer id not found in message")


if __name__ == "__main__":
    print("On-call Agent Demo Started")
    print("Type 'exit' to stop")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        try:
            result = run_agent(user_input)
            print("\nAgent:")
            print(json.dumps(result, indent=2, default=str))
        except Exception as ex:
            print("\nAgent Error:")
            print(str(ex))