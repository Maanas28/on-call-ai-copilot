from sanic import Sanic, json
from sanic.request import Request

from app.service import (
    list_open_incidents,
    get_incident_details,
    acknowledge_incident,
    assign_to_engineer,
    add_resolution_note,
    resolve_incident,
)

app = Sanic("oncall_demo")


@app.get("/health")
async def health(_: Request):
    return json({"status": "ok"})


@app.get("/incidents")
async def get_open_incidents(_: Request):
    return json({"incidents": list_open_incidents()})


@app.get("/incidents/<incident_id:str>")
async def get_incident(_: Request, incident_id: str):
    try:
        return json(get_incident_details(incident_id))
    except ValueError as ex:
        return json({"error": str(ex)}, status=404)


@app.post("/incidents/<incident_id:str>/acknowledge")
async def acknowledge(_: Request, incident_id: str):
    try:
        return json(acknowledge_incident(incident_id))
    except ValueError as ex:
        return json({"error": str(ex)}, status=400)


@app.post("/incidents/<incident_id:str>/assign")
async def assign(request: Request, incident_id: str):
    try:
        body = request.json or {}
        engineer_id = body.get("engineer_id")
        if not engineer_id:
            return json({"error": "engineer_id is required"}, status=400)

        return json(assign_to_engineer(incident_id, engineer_id))
    except ValueError as ex:
        return json({"error": str(ex)}, status=400)


@app.post("/incidents/<incident_id:str>/notes")
async def add_note(request: Request, incident_id: str):
    try:
        body = request.json or {}
        note = body.get("note")
        if not note:
            return json({"error": "note is required"}, status=400)

        return json(add_resolution_note(incident_id, note))
    except ValueError as ex:
        return json({"error": str(ex)}, status=400)


@app.post("/incidents/<incident_id:str>/resolve")
async def resolve(_: Request, incident_id: str):
    try:
        return json(resolve_incident(incident_id))
    except ValueError as ex:
        return json({"error": str(ex)}, status=400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, dev=True)