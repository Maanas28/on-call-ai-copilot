# On-Call AI Copilot (Agent-based Incident Management System)

## 1. Overview

**On-Call AI Copilot** is a proof-of-concept project that demonstrates how an AI agent can autonomously manage incident workflows using a tool-based architecture powered by **Model Context Protocol (MCP)**.

This project is not designed as a traditional chatbot. The main objective is to show how AI can move beyond answering questions and instead take meaningful actions against a system by calling well-defined tools.

The project simulates a real-world on-call support environment where incidents can be listed, inspected, acknowledged, assigned, updated with notes, and resolved through either REST APIs or MCP tools.

---

## 2. Project Objective

The objective of this project is to demonstrate an architecture where an AI agent can interact with operational systems through controlled tools.

The POC focuses on the following goals:

- Simulate common incident management workflows.
- Expose backend operations as MCP tools.
- Allow an AI agent to decide which tool should be called based on user intent.
- Demonstrate the difference between a normal chatbot and an action-oriented AI agent.
- Provide a clean architecture that separates REST APIs, business logic, MCP tools, and agent behavior.

---

## 3. Why This Project Matters

Traditional chatbots usually respond with suggestions such as:

> “You should acknowledge the incident and assign it to an engineer.”

The On-Call AI Copilot demonstrates a more advanced approach where the AI can actually perform the workflow:

> “I found the open incident, acknowledged it, assigned it to Priya, added a note, and resolved it.”

This makes the project useful for demonstrating how AI can support real operational workflows when connected to reliable backend tools.

---

## 4. High-Level Architecture

The project is organized into four main layers:

```text
User Input
   |
   v
Agent Layer
   |
   v
MCP Tools
   |
   v
Service Layer
   |
   v
In-Memory Incident Store
```

The same service layer is shared by both REST APIs and MCP tools. This ensures that the business logic stays centralized and consistent across different access methods.

---

## 5. Core Components

### 5.1 Backend API Layer

The backend is built using **Python** and **Sanic**.

It exposes REST APIs for incident management operations. These APIs are mainly used for manual testing and for demonstrating that the system can also behave like a normal backend service.

Supported REST operations include:

- List open incidents
- Get incident details
- Acknowledge an incident
- Assign an incident to an engineer
- Add a resolution note
- Resolve an incident

REST APIs are tested using **Postman**.

---

### 5.2 Service Layer

The service layer contains the core business logic of the application.

Responsibilities of the service layer include:

- Fetching open incidents
- Finding incident details by ID
- Updating incident status
- Assigning incidents to engineers
- Adding notes to incidents
- Resolving incidents

This layer is intentionally shared between the REST API layer and the MCP server. This avoids duplicate logic and keeps the architecture clean.

For this POC, the service layer uses in-memory mock data instead of a database.

---

### 5.3 MCP Server Layer

The MCP server is built using the **MCP Python SDK**.

It exposes incident management operations as tools that can be called by an AI agent or tested using MCP Inspector.

Available MCP tools include:

| Tool Name | Purpose |
|---|---|
| `list_open_incidents` | Returns all currently open incidents. |
| `get_incident_details` | Returns full details for a specific incident. |
| `acknowledge_incident` | Marks an incident as acknowledged. |
| `assign_to_engineer` | Assigns an incident to a specific engineer. |
| `add_resolution_note` | Adds an investigation or resolution note. |
| `resolve_incident` | Marks an incident as resolved. |

The MCP layer is important because it allows the AI agent to interact with backend functionality in a structured and controlled way.

---

### 5.4 Agent Layer

The agent layer is responsible for receiving user input, deciding what action should be taken, calling the appropriate tool, and returning the result.

The project supports two planned versions of the agent.

#### Version 1: Rule-Based Agent

The first version uses simple conditional logic.

Example:

```text
If the user says "show open incidents",
call list_open_incidents.

If the user says "assign incident INC-001 to Priya",
call assign_to_engineer.
```

This version is useful for demonstrating the workflow without requiring an LLM.

#### Version 2: LLM-Based Agent

The second version uses an LLM with function calling.

In this version, the LLM interprets the user request, selects the correct tool, provides the required parameters, and executes the action through the MCP tool layer.

This version demonstrates the real value of AI-driven automation.

---

## 6. Example Workflow

A typical incident workflow may look like this:

```text
User: Show me all open incidents.
Agent: Calls list_open_incidents.

User: Get details for INC-001.
Agent: Calls get_incident_details.

User: Acknowledge this incident.
Agent: Calls acknowledge_incident.

User: Assign it to Priya.
Agent: Calls assign_to_engineer.

User: Add note: Restarted payment service and monitoring recovery.
Agent: Calls add_resolution_note.

User: Resolve the incident.
Agent: Calls resolve_incident.
```

This demonstrates that the AI is not only generating text, but also performing real operations through tools.

---

## 7. Testing Strategy

### REST API Testing

REST APIs are tested using **Postman**.

Postman is useful for validating backend endpoints directly and confirming that the incident service works correctly.

### MCP Tool Testing

MCP tools are tested using **MCP Inspector**.

MCP Inspector is useful for verifying that tools are exposed correctly, tool schemas are valid, parameters are accepted properly, and tool responses are returned as expected.

---

## 8. Difference Between REST APIs, MCP Tools, and Agent

| Layer | Purpose |
|---|---|
| REST API | Allows humans or external systems to call backend operations directly. |
| MCP Tools | Exposes backend operations in a tool format that AI agents can understand and call. |
| Agent | Decides which tool to call based on user intent and coordinates the workflow. |

REST APIs show that the backend works.

MCP tools make backend actions available to AI.

The agent connects user intent with tool execution.

---

## 9. Current Scope

This project is currently a proof of concept.

Included in the current scope:

- Python Sanic backend
- REST APIs for incident operations
- Shared service layer
- In-memory mock incident store
- MCP server exposing incident tools
- MCP Inspector testing
- Rule-based agent
- Planned LLM-based agent using function calling

---

## 10. Out of Scope

The following items are intentionally not included in the current POC:

- Authentication and authorization
- Database persistence
- External incident management integrations
- Slack, Teams, PagerDuty, or Jira integration
- Production monitoring
- Audit logging
- Role-based access control
- Deployment automation

These can be added in future iterations once the core concept is validated.

---

## 11. Future Enhancements

Possible future improvements include:

- Add database support for persistent incident storage.
- Add authentication and authorization.
- Integrate with PagerDuty, Jira, Slack, or Teams.
- Add audit logs for every tool action.
- Add approval workflows before resolving incidents.
- Add severity-based routing logic.
- Add LLM-based reasoning for incident triage.
- Add automated incident summaries.
- Add post-incident report generation.
- Add deployment using Docker.

---

## 12. Demo Value

This POC is valuable because it clearly demonstrates the architecture of an action-oriented AI system.

It shows how:

- Backend capabilities can be exposed as tools.
- AI agents can safely interact with systems through controlled interfaces.
- Business logic can remain centralized in a service layer.
- REST APIs and MCP tools can reuse the same backend logic.
- AI can participate in operational workflows instead of only providing recommendations.

---

## 13. Summary

On-Call AI Copilot is a focused POC that demonstrates how AI can operate incident management workflows through MCP tools.

The project highlights the shift from chatbot-style assistance to tool-driven AI automation. It provides a strong foundation for demonstrating agentic AI concepts in a practical engineering context.

The current implementation is intentionally simple and demo-friendly, while the architecture leaves room for future production-grade enhancements such as persistence, authentication, integrations, and auditability.

