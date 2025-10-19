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
new_title = "ProductServer"
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

@mcp.tool(name="GetProducts",title="Get the Products",description="Get the list of products available")
def GetProducts()-> dict:
    """
    Get the list of products available
    """
    return callRESTAPI(BASE_URL+"products/")

@mcp.tool(name="GetProductsById",title="Get the specific Product by product id",description="Get the specific Product by product id")
def GetProductsById(prod_id:str)-> dict:
    """
    Get the specific Product by product id
    """
    return callRESTAPI(BASE_URL+"products/"+prod_id)

@mcp.tool(name="GetProductsByCategory",title="Get the list of Products by category",description="Get the list of Products by category")
def GetProductsByCategory(category:str)-> dict:
    """
    Get the list of Products by category
    """
    print("called=GetProductsByCategory")
    response=[]
    response=callRESTAPI(BASE_URL+"products/category/"+category)
    final_response=[]
    print("+"*100)
    print(response,len(response))
    print("+"*100)

    if len(response)==0:
        categories=["men's clothing","women's clothing"]
        mens_response=callRESTAPI(BASE_URL+"products/category/"+categories[0])
        # print("MENS CLOTHING")
        # print(mens_response)
        # print("+"*100)
        womens_response=callRESTAPI(BASE_URL+"products/category/"+categories[1])
        # print("WOMENS CLOTHING")
        # print(womens_response)
        # print("+"*100)
        final_response.append(mens_response)
        final_response.append(womens_response)
        response=final_response
        print("!"*100)
        print(response)
        print("!"*100)
    print("&"*100)
    print(response)
    print("&"*100)
    return response

@mcp.tool(name="GetAllCategories",title="Get the list of Product Categories",description="Get the list of Product Categories")
def GetAllCategories()-> dict:
    """
    Get the list of Product Categories
    """
    print("called=GetAllCategories")
    final_response=[]
    response=callRESTAPI(BASE_URL+"products/categories")
    for _category in response:
        _currenturl=BASE_URL+"products/category/"+_category
        final_response.append("<a href='"+_currenturl+"' target='_blank'>"+_category+"</a>")
    return response

@mcp.tool(name="GetProductsBySeason",title="Get the list of Product suitable for Season",description="Get the list of Product suitable for Season")
def GetProductsBySeason(season:str)-> dict:
    """
    Get the list of Product suitable for Season
    """
    print("CALLED:",GetProductsBySeason,"Season=",season)
    season=season.lower().strip()
    if season=="fall":
        season="Autumn"
    response=callRESTAPI(BASE_URL+"products")
    final_response=[]
    for _info in response:
        if season.lower() in _info["title"].lower() or season.lower() in _info["description"].lower():
            final_response.append(_info)
    print("AFTER FILTER")
    print(final_response)
    return final_response

@mcp.tool(name="GetProductsByWeather",title="Get the list of Product suitable for Weather",description="Get the list of Product suitable for Weather")
def GetProductsBySeason(weather)-> dict:
    """
    Get the list of Product suitable for Weather
    """
    final_response=callRESTAPI(BASE_URL+"products/1")
    # for _info in response:
    #     if season.lower() in _info["title"].lower() or season.lower() in _info["description"].lower():
    #         final_response.append(_info)
    return final_response

@mcp.tool(name="GetProductsByTitle",title="Get the list of Product by matching the Title",description="Get the list of Product by matching the Title")
def GetProductsByTitle(title:str)-> dict:
    """
    Get the list of Product by matching the Title
    Args:
        title: exact or part of the title
    """
    response=callRESTAPI(BASE_URL+"products")
    final_response=[]
    for _info in response:
        if title.lower() in _info["title"].lower():
            final_response.append(_info)
    return final_response

@mcp.tool(name="GetProductsByDescription",title="Get the list of Product by matching the Description",description="Get the list of Product by matching the Description")
def GetProductsByDescription(description:str)-> dict:
    """
    Get the list of Product by matching the Description
    Args:
        description: a word or few words about the product
    """
    response=callRESTAPI(BASE_URL+"products")
    final_response=[]
    for _info in response:
        if description.lower() in _info["description"].lower():
            final_response.append(_info)
    return final_response


def callRESTAPI(url):
    final_response={}
    try:
        response = requests.get(url)
        if response.status_code not in [200,201]:
            final_response= {"error": f"Login failed: {response.status_code} {response.text}"}
        else:
            final_response = response.json()
        return final_response
    except Exception as e:
        return {"error": str(e)}
    

response_queue: asyncio.Queue = asyncio.Queue()

# @app.api_route("/sse", methods=["GET", "POST"])
# async def mcp_stream(request: Request):
#     """
#     Unified MCP endpoint using streamable-http transport.
#     Client must send 'Accept: text/event-stream'.
#     """
#     if request.method == "GET":
#         # Host is opening an event stream
#         async def event_generator():
#             async for message in mcp.stream_messages():
#                 yield f"data: {json.dumps(message)}\n\n"
#         return StreamingResponse(event_generator(), media_type="text/event-stream")

#     elif request.method == "POST":
#         # Host sends JSON-RPC request
#         body = await request.json()
#         response = await mcp.dispatch(body)
#         if response:
#             await mcp.push_message(response)
#         return {"status": "ok"}

# @app.get("/")
# async def healthcheck():
#     return {"status": "ok", "message": "MCP Auth Server running with SSE transport"}


#print(GetProductsByWeather("winter"))

if __name__=="__main__":
    mcp.settings.host=SERVER_HOST
    mcp.settings.port=int(str(SERVER_PORT))
    mcp.run(transport=SERVER_MODE)