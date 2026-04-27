import asyncio

from llm_agent.llm_agent import run_agent
from llm_agent.mcp_client import close_mcp_session, start_mcp_session


async def main():
    print("On-call LLM Agent started with MCP integration.")
    print("Type 'exit' to stop.")

    session, session_context, stdio_context = await start_mcp_session()

    try:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Agent stopped.")
                break

            try:
                response = await run_agent(user_input, session)
                print(f"\nAgent: {response}")
            except Exception as error:
                print(f"\nError: {error}")

    finally:
        await close_mcp_session(session_context, stdio_context)


if __name__ == "__main__":
    asyncio.run(main())