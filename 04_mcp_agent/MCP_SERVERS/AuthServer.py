#uvicorn AuthServer:app --host 127.0.0.1 --port 8000 --reload
import asyncio
import json
import jwt
import uvicorn
import requests,os
from fastapi.responses import StreamingResponse
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import server as MCPSERVER

from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
new_title = "AuthServer"
os.system(f"title {new_title}")

def getCurrentFileName():
    current_file_path = __file__
    file_name_with_extension = os.path.basename(current_file_path)
    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
    #print("file_name_without_extension",file_name_without_extension)
    return file_name_without_extension

filenameforconfig=getCurrentFileName().lower().strip().replace(" ","")
#print("filenameforconfig=",filenameforconfig)
env_file_name=".env.mcp."+filenameforconfig
#print("env_file_name=",os.getcwd()+"\\"+env_file_name.strip())
load_dotenv(os.getcwd()+"\\"+env_file_name,override=True)

BASE_URL=os.getenv("BASE_URL")
ADMIN_USER = os.getenv("ADMIN_USER")#,"admin@gmail.com"
SERVER_MODE=os.getenv("SERVER_MODE")#,"SSE"
SERVER_HOST=os.getenv("SERVER_HOST")#,"127.0.0.1"
SERVER_PORT=os.getenv("SERVER_PORT")#8000
#print(BASE_URL,ADMIN_USER,SERVER_MODE,SERVER_HOST,SERVER_PORT)
mcp = FastMCP("Auth")
app=FastAPI()

# Simple in-memory token store
TOKENS = {}

@mcp.tool(name="Authenticate",title="Authenticate User",description="Authenticate user with FakeStoreAPI and return JWT token.")
def Authenticate(username: str, password: str) -> dict:
    """
    Authenticate user with FakeStoreAPI and return JWT token.
    """
    final_response={}
    url = BASE_URL+"auth/login/"
    payload={}
    payload["username"]=username
    payload["password"]=password
    try:
        print("requesting",url,"payload=",payload)
        response = requests.post(url, data=payload)
        if response.status_code not in [200,201]:
            final_response= {"error": f"Login failed: {response.status_code} {response.text}"}
        else:
            data = response.json()
            token = data.get("token")
            TOKENS[username] = token
            user_profile=UserProfile(token)
            final_response={"username": username, "token": token,"profile":user_profile}
        return final_response
    except Exception as e:
        return {"error": str(e)}
    
@mcp.tool(name="UserProfile",title="UserProfile",description="Get User Profile of an authenticated user by Token")
def UserProfile(token: str) -> dict:
    """
    Get User Profile of an authenticated user by  JWT token.
    """
    final_response={}
    _decoded_token=jwt.decode(jwt=token,options={"verify_signature": False},algorithms="HS256")
    _id=_decoded_token["sub"]
    url = BASE_URL+"users/"+str(_id)
    try:
        print("requesting",url)
        response = requests.get(url)
        if response.status_code not in [200,201]:
            final_response= {"error": f"Getting User Profile failed: {response.status_code} {response.text}"}
        else:
            final_response = response.json()
        return final_response
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def Authorise(username: str, action: str) -> dict:
    """
    Authorise user for product operations.
    Only admin@retailstore can add/delete products.
    """
    if username == ADMIN_USER:
        return {"authorised": True, "action": action}
    else:
        return {"authorised": False, "error": "Not allowed"}


response_queue: asyncio.Queue = asyncio.Queue()

@app.api_route("/mcp", methods=["GET", "POST"])
async def mcp_stream(request: Request):
    """
    Unified MCP endpoint using streamable-http transport.
    Client must send 'Accept: text/event-stream'.
    """
    if request.method == "GET":
        # Host is opening an event stream
        async def event_generator():
            async for message in mcp.stream_messages():
                yield f"data: {json.dumps(message)}\n\n"
        return StreamingResponse(event_generator(), media_type="text/event-stream")

    elif request.method == "POST":
        # Host sends JSON-RPC request
        body = await request.json()
        response = await mcp.dispatch(body)
        if response:
            await mcp.push_message(response)
        return {"status": "ok"}

@app.get("//")
async def healthcheck(request: Request):
    return displaytools()

def displaytools():
    _list=asyncio.run(mcp.list_tools())
    _tools=[]

    for _tool in _list:
        item={"Tool Name":_tool.name,"Description":_tool.description,"properties":_tool.inputSchema}
        _tools.append(item)
    return _tools

if __name__=="__main__":  
    mcp.settings.host=SERVER_HOST
    mcp.settings.port=int(str(SERVER_PORT))
    mcp.run(transport=SERVER_MODE)