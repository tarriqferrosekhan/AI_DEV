import streamlit as st
import json,os
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
import asyncio
from openai import AsyncOpenAI, OpenAI
import os
from dotenv import load_dotenv

class Utils:
    class Key:
        MODE_CMD="CMD"
        MODE_UI="UI"

class MCPHost:
    def __init__(self):
        self.Title="MCP_HOST"
        self.Server_Atomic=True
        self.Server_Status="NOT_STARTED"
        self.Tools=[]
        self.openai_client=None
        self.OPENAI_MODEL=None
        self.Ready=False
        self.PROMPT="""Stick only to this instruction and do not think outside the context.
        You are a reasoning agent that can call multiple tools when needed.
        If user is looking for products based on weather, call all the applicable tools.
        If user is wants to place the order call the Or
        """
        self.Messages=[{"role": "system", "content": self.PROMPT}]
        self.LogMessages=[]
        self.mcp_servers={
        "AuthServer":{"url":"http://127.0.0.1:8001/sse"},
        "WeatherServer":{"url":"http://127.0.0.1:8002/sse"},
        "ProductsServer":{"url":"http://127.0.0.1:8003/sse"},
        }
        self.init()

    def showMessage(self,*args):
        final_message=""
        for message in args:
            final_message=final_message+message
        print(final_message)

    def init(self):
        load_dotenv(".env.host")
        os.system(f"title {self.Title}")
        self.OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise RuntimeError("Set OPENAI_API_KEY in your environment")
        self.openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


    def logmessage(self,message,messageType="Info",displayMessage=True):
        self.LogMessages.append({"message":message,"messageType":messageType})
        if displayMessage:
            print(message)
        
    def logerror(self,message):
        self.logmessage(message=message,messageType="ERROR")


    def getHostStatus(self):
        HostErrorStatus = [item for item in self.LogMessages if item["messageType"].lower() == "error"]
        print("HostErrorStatus=",HostErrorStatus)

        if len(HostErrorStatus)>0:
            if self.Server_Atomic==True:
                self.Server_Status="NOT_READY"
            else:
                self.Server_Status="WARNING"
        else:
            self.Server_Status="STARTED"
        return self.Server_Status

    def displayTools(self,Tools):
        print("="*100)
        print("Tools:")
        print("="*100)
        for _tool in Tools:
            _server_name=_tool.get("function")["server_name"]
            _server_url=_tool.get("function")["server_url"]
            _function_name=_tool.get("function")["name"]
            _description=_tool.get("function")["description"]
            print(_server_name,"|",_server_url,"|",_function_name,"|",_description)
        print("="*100)
    
    async def getLLMResponse(self):
        response=await self.openai_client.chat.completions.create(
                    model=self.OPENAI_MODEL,
                    messages=self.Messages,
                    tools=self.Tools
                    ,parallel_tool_calls=True
                    ,tool_choice="auto"
                    ,max_tokens=800
                )
        return response

    async def connect_to_servers(self):
        print("Connecting Servers...")
        for server in self.mcp_servers.keys():
            try:
                server_url=self.mcp_servers[server]["url"]
                client=Client(server_url)
                async with client:
                    self.logmessage(server+" connected successfully")
                    tools=await client.list_tools()
                    for _tool in tools:
                        name=_tool.name
                        description=_tool.description or "No description provided"
                        input_schema=_tool.inputSchema or {"type": "object", "properties": {}}
                        self.Tools.append({
                        "type": "function",
                        "function": {
                            "name": name,
                            "description": description,
                            "parameters": input_schema,
                            "server_url":server_url,
                            "server_name":server
                        }
                        })
            except:
                self.logerror("Error Connecting MCP Server="+server)
        self.Server_Status=self.getHostStatus()
        print("HOST_STATUS=",self.Server_Status)
        # if self.Server_Status=="STARTED":
        #     self.displayTools(self.Tools)
        return {"status":self.Server_Status,"Tools":self.Tools}

    async def call_tool(self,server_url, tool_name, arguments):
        """Actually invoke a tool on the target MCP server."""
        print("trying to Invoke tool")
        print("Server_url=",server_url, "tool=",tool_name,"args=",arguments)
        async with Client(server_url) as client:
            result=[]
            response = await client.call_tool_mcp(tool_name, arguments)
            if response.isError==False:
                if response.content!=None and len(response.content)>0:
                    print("response.content:")
                    print(response.content)
                    for _content in response.content:
                        _text=_content.text
                        if isinstance(_text,dict):
                            result.append(json.loads(_text))
                        elif isinstance(_text,str):
                            result.append(_text)
            print("FINAL TOOL CALL RESULT")
            print(result)
            return result

    async def process_call_tools(self,chat_response_message):
        for tool_call in chat_response_message.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"\n🛠️  Server Tool requested: {tool_name} | Args: {args}")

            # Find server URL for this tool
            server_url = None
            for t in self.Tools:
                if t["function"]["name"] == tool_name:
                    server_url = t["function"]["server_url"]
                    break

            if not server_url:
                print(f"⚠️ Could not find server for tool {tool_name}")
                continue

            result = await self.call_tool(server_url, tool_name, args)
            print(f"✅ Tool result: {result}")

            # Step 3: Feed tool result back to model for final answer
            self.Messages.append(chat_response_message)
            self.Messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": json.dumps(result)
            })
            final_resp = await self.getLLMResponse() 
            print("\n💬 Final Response:")
            print(final_resp.choices[0].message.content)
            return final_resp.choices[0].message.content

    async def chat_with_tools(self,query):
        # --- first request ---
        response={}
        self.Messages.append({"role": "user", "content": query})
        chat_resp=await self.getLLMResponse()
        print("chat_resp.choices[0].message")
        chat_response_message=chat_resp.choices[0].message
        print(chat_resp.choices[0].message)
        if hasattr(chat_response_message, "tool_calls") and chat_response_message.tool_calls:
            response=await self.process_call_tools(chat_response_message)
        else:
            print("\n💬 Model replied directly:")
            print(chat_response_message)
            response=chat_response_message.content
        return response

async def main():
    mcphost=MCPHost()
    print("🔗 Connecting to MCP servers...")
    await mcphost.connect_to_servers()
    print(f"\n🧩 Registered tools: {[t['function']['name'] for t in mcphost.Tools]}")
    # Example queries:
    await mcphost.chat_with_tools()
    # await chat_with_tools("Authenticate user JohnDoe", manual_tool="auth_user")

if __name__ == "__main__":
    asyncio.run(main())
