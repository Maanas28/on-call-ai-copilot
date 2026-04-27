import json
from typing import Any

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

from llm_agent.trace_logger import log_step


def build_mcp_server_params() -> StdioServerParameters:
    return StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )


def convert_mcp_tools_to_llm_tools(mcp_tools: list[types.Tool]) -> list[dict[str, Any]]:
    llm_tools = []

    for tool in mcp_tools:
        llm_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema,
                },
            }
        )

    return llm_tools


async def parse_mcp_tool_result(result) -> Any:
    if getattr(result, "structuredContent", None):
        return result.structuredContent

    parsed_content = []

    for content in result.content:
        if isinstance(content, types.TextContent):
            text = content.text

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                parsed_content.append(text)

    if len(parsed_content) == 1:
        return parsed_content[0]

    return parsed_content


async def call_mcp_tool(
    session: ClientSession,
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:
    log_step(
        "5. MCP CLIENT CALL",
        "Calling selected tool through the MCP server.",
        {
            "tool_name": tool_name,
            "arguments": arguments,
        },
    )

    result = await session.call_tool(tool_name, arguments=arguments)

    parsed_result = await parse_mcp_tool_result(result)

    log_step(
        "6. MCP TOOL RESULT",
        "MCP server returned the tool execution result.",
        {
            "tool_name": tool_name,
            "result": parsed_result,
        },
    )

    return parsed_result


async def start_mcp_session():
    server_params = build_mcp_server_params()

    log_step(
        "MCP SERVER START",
        "Starting MCP server as a stdio subprocess.",
        {
            "command": server_params.command,
            "args": server_params.args,
        },
    )

    stdio_context = stdio_client(server_params)
    read_stream, write_stream = await stdio_context.__aenter__()

    session_context = ClientSession(read_stream, write_stream)
    session = await session_context.__aenter__()

    await session.initialize()

    log_step(
        "MCP SESSION INITIALIZED",
        "MCP client successfully initialized the session with the server.",
    )

    return session, session_context, stdio_context


async def close_mcp_session(session_context, stdio_context):
    await session_context.__aexit__(None, None, None)
    await stdio_context.__aexit__(None, None, None)

    log_step(
        "MCP SESSION CLOSED",
        "MCP client session and server subprocess were closed.",
    )