"""End-to-end MCP client test: spawn server.py over stdio and exercise tools."""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    params = StdioServerParameters(command="./venv/bin/python", args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            info = await session.initialize()
            print("CONNECTED to:", info.serverInfo.name)

            tools = await session.list_tools()
            print("TOOLS:", [t.name for t in tools.tools])

            print("\n-- list_voices --")
            r = await session.call_tool("list_voices", {})
            print(r.content[0].text[:200])

            print("\n-- speak_text (empty) --")
            r = await session.call_tool("speak_text", {"text": "   "})
            print(r.content[0].text)

            print("\n-- speak_text (real) --")
            r = await session.call_tool(
                "speak_text",
                {"text": "Task complete. Tests passed.", "rate": 160, "volume": 0.9},
            )
            print(r.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
