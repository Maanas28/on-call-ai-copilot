import json

from mcp import ClientSession

from llm_agent.llm_client import client
from llm_agent.mcp_client import call_mcp_tool, convert_mcp_tools_to_llm_tools
from llm_agent.trace_logger import log_step


MODEL_NAME = "llama3.1:8b"


SYSTEM_PROMPT = """
You are an AI on-call incident management assistant.

You can manage incidents by calling MCP tools.

Rules:
- Use tools for incident operations.
- Do not invent incident IDs.
- Do not invent engineer IDs.
- If the user asks to list, get, acknowledge, assign, add note, or resolve an incident, call the correct tool.
- After a tool is executed, summarize the result clearly.
"""


async def run_agent(user_input: str, mcp_session: ClientSession) -> str:
    log_step(
        "1. USER INPUT",
        "The user entered a natural language request.",
        {
            "user_input": user_input,
        },
    )

    tools_response = await mcp_session.list_tools()
    llm_tools = convert_mcp_tools_to_llm_tools(tools_response.tools)

    log_step(
        "2. MCP TOOL DISCOVERY",
        "Fetched available tools from the MCP server and converted them to LLM tool schema.",
        {
            "mcp_tools": [tool.name for tool in tools_response.tools],
        },
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    log_step(
        "3. LLM REQUEST",
        "Sending user input and MCP-discovered tool definitions to the local Ollama LLM.",
        {
            "model": MODEL_NAME,
            "available_tools": [
                tool["function"]["name"]
                for tool in llm_tools
            ],
        },
    )

    first_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=llm_tools,
        tool_choice="auto",
    )

    assistant_message = first_response.choices[0].message

    if not assistant_message.tool_calls:
        log_step(
            "NO TOOL SELECTED",
            "The LLM did not select any MCP tool.",
            {
                "response": assistant_message.content,
            },
        )

        return assistant_message.content or "No tool call was selected."

    messages.append(assistant_message)

    executed_tools = []

    for tool_call in assistant_message.tool_calls:
        tool_name = tool_call.function.name
        raw_arguments = tool_call.function.arguments or "{}"
        arguments = json.loads(raw_arguments)

        log_step(
            "4. TOOL SELECTED BY LLM",
            "The LLM selected an MCP tool based on the user's request.",
            {
                "tool_name": tool_name,
                "arguments": arguments,
            },
        )

        result = await call_mcp_tool(
            session=mcp_session,
            tool_name=tool_name,
            arguments=arguments,
        )

        executed_tools.append(
            {
                "tool": tool_name,
                "arguments": arguments,
                "result": result,
            }
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            }
        )

    log_step(
        "7. FINAL LLM REQUEST",
        "Sending MCP tool result back to the LLM for final user-friendly response.",
        {
            "executed_tools": executed_tools,
        },
    )

    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
    )

    final_message = final_response.choices[0].message.content

    log_step(
        "8. FINAL RESPONSE",
        "The LLM generated the final response for the user.",
        {
            "final_response": final_message,
        },
    )

    if final_message:
        return final_message

    return json.dumps(executed_tools, indent=2, default=str)