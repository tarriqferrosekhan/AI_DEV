import asyncio
import sys
import os
import json
from typing import Optional, List, Dict, Any
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in your environment")

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


class MCPClientOpenAI:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.stdio = None
        self.write = None

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server (stdio transport)."""
        command = "python" if server_script_path.endswith(".py") else "node"
        server_params = StdioServerParameters(command=command, args=[server_script_path])

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\n✅ Connected to server with tools:", [tool.name for tool in tools])

    def _tools_to_openai_tools(self, tools: List[Dict[str, Any]]):
        """
        Convert MCP tool descriptors into OpenAI 'tools' schema.
        """
        result = []
        for t in tools:
            name = t.get("name")
            description = t.get("description") or "No description provided"
            input_schema = t.get("inputSchema") or {"type": "object", "properties": {}}
            result.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": input_schema
                }
            })
        return result

    async def process_query(self, query: str) -> str:
        """Process a user query using OpenAI + MCP tools."""
        if not self.session:
            raise RuntimeError("Not connected to MCP server.")

        # fetch available tools
        resp = await self.session.list_tools()
        tools_info = [{
            "name": tool.name,
            "description": tool.description,
            "inputSchema": getattr(tool, "inputSchema", {"type": "object", "properties": {}})
        } for tool in resp.tools]

        tools = self._tools_to_openai_tools(tools_info)

        # conversation state
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": "You are a helpful assistant that can call tools when needed."},
            {"role": "user", "content": query}
        ]

        # --- first request ---
        chat_resp = await openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=800
        )

        assistant_msg = chat_resp.choices[0].message
        messages.append(assistant_msg)

        final_parts = []

        if assistant_msg.tool_calls:
            # handle each tool call
            for tool_call in assistant_msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments or "{}")

                try:
                    tool_result = await self.session.call_tool(fn_name, fn_args)
                    tool_output = getattr(tool_result, "content", str(tool_result))
                except Exception as e:
                    tool_output = f"Tool call failed: {e}"

                # append tool result properly with tool_call_id
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_output)
                })

            # --- second request (follow-up) ---
            followup = await openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=800
            )
            followup_text = followup.choices[0].message.content or ""
            final_parts.append(followup_text)
        else:
            # no tool call, just plain response
            final_parts.append(assistant_msg.content or "")

        return "\n".join(final_parts)

    async def chat_loop(self):
        print("\n💬 MCP OpenAI Client Started!")
        print("Type your queries or 'quit' to exit.\n")

        while True:
            try:
                query = input("Query: ").strip()
                if query.lower() == "quit":
                    break
                response = await self.process_query(query)
                print("\nAssistant:", response)
            except Exception as e:
                print(f"\n❌ Error: {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client_openai.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClientOpenAI()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
