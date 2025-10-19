import asyncio
import json,os
import streamlit as st
from host import MCPHost
import re
import openai
from llama_index.core.tools import FunctionTool
import llama_index.core.agent as llamagent
from llama_index.llms.openai import OpenAI

openai_api_key=os.environ.get("OPENAI_API_KEY")
openai.api_key=openai_api_key
mcphost=MCPHost()

st.set_page_config(page_title="MCP Agent Demo", page_icon=None, layout=None, initial_sidebar_state=None, menu_items=None)
st.info("MCP Agent Demo")

def UI_LoginUser()->dict:
    """user login"""
    st.session_state.ui_action = "login_user"
    result = {}
    result["action_type"]="UI"
    result["action"]="login_user"
    result["msg"]= f"Open login dialog"
    return result

def UI_addToCart()->dict:
    """user login"""
    st.session_state.ui_action = "addTo_Cart"
    result = {}
    result["action_type"]="UI"
    result["action"]="addTo_Cart"
    result["msg"]= f"Open addToCart dialog"
    return result

async def Chat_WithLLM():
    st.session_state.ui_action = "Chat With LLM"
    result = {}
    result["action_type"]="CHAT"
    result["action"]="chat_with_LLM"
    result["msg"]= f"chat with LLM"
    return result

@st.dialog("Sign in")
def showSignInUser():
    st.write("show")
    _user_name=st.text_input("User name")
    _password=st.text_input("Password",type="password")
    if st.button("Login"):
        if _user_name and _password:
            chat_response=asyncio.run(mcphost.chat_with_tools("Authenticate user_name="+_user_name+" password="+_password))
            st.write(chat_response)
            st.rerun()

@st.dialog("add To Cart")
def showaddToCart():
    st.write("CART")
    if st.button("close"):
        st.rerun()

def ui_tool_call(ui_action_response):
    Tool_Name=""
    if ui_action_response["action"]=="login_user":
        showSignInUser()
        Tool_Name="showSignInUser"
    st.session_state.chat_messages.append({"role": "assistant", "content":"Tool "+Tool_Name+" called." })

UI_PROMPT = f"""
You are the UI Agent Assistant.
You will try to understand the intent of the user first. 
If user tries to perform one of the UI actions call the tools that starts with UI_ otherwise call the Chat_ Tool
User Action that needs UI_ Tools to be called: 
- Login
- Sign in 
- add to cart (if not already signed in)
- Register
- Authenticate
- Sign up
- provide username and password
For 

User Action t
If user is trying to sign in, login or add to cart,   
- login, sign in , sing up 

- If the user wants to authenticate, login, sign in, enter user name or enter password show the LoginTool.
- 
"""

UITOOLS = [
    FunctionTool.from_defaults(fn=UI_LoginUser,description="user login",return_direct=True,),
    FunctionTool.from_defaults(fn=UI_addToCart,description="use this tool to add product to the user's shopping cart",return_direct=True,),
    FunctionTool.from_defaults(fn=Chat_WithLLM,description="Product, Category, Weather related queries",return_direct=True,),

]

llm = OpenAI(model="gpt-4o-mini", temperature=0,api_key=openai_api_key)

uiagent_react = llamagent.FunctionAgent(
    tools=UITOOLS,
    llm=llm,
    verbose=True,
    system_prompt=UI_PROMPT,
)


if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

def is_image_url(url):
    return re.match(r".*\.(jpg|jpeg|png|gif|bmp|webp|svg)$", url, re.IGNORECASE)

def display_mcp_response(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                st.subheader(k)
                display_mcp_response(v)
            elif isinstance(v, str) and is_image_url(v):
                st.image(v, caption=k)
            else:
                st.write(f"**{k}:** {v}")
    elif isinstance(data, list):
        for item in data:
            display_mcp_response(item)
    elif isinstance(data, str):
        urls = re.findall(r"(https?://\S+\.(?:jpg|jpeg|png|gif|bmp|webp|svg))", data)
        for url in urls:
            st.image(url)
    else:
        st.write(data)

def extract_flat_json_strings(s):
    candidates = re.findall(r'(\{.*?\}|\[.*?\])', s)
    valid_json = {}
    for candidate in candidates:
        try:
            candidate=candidate.replace("'","\"")
            valid_json=json.loads(candidate)
            break
        except json.JSONDecodeError:
            continue
    return valid_json

def extract_all_nested_jsons(s):
    json_strings = []
    stack = []
    start_idx = None

    for i, char in enumerate(s):
        if char in ['{', '[']:
            if not stack:
                start_idx = i  # Potential start of a JSON
            stack.append(char)
        elif char in ['}', ']']:
            if stack:
                open_char = stack.pop()
                if ((open_char == '{' and char != '}') or 
                    (open_char == '[' and char != ']')):
                    # Mismatched brackets/braces, reset
                    stack = []
                    start_idx = None
                    continue
                if not stack:
                    # Potential full JSON string found
                    candidate = s[start_idx:i+1]
                    try:
                        candidate=candidate.replace("'","\"")
                        json.loads(candidate)
                        json_strings.append(candidate)
                    except json.JSONDecodeError:
                        pass
                    start_idx = None  # Reset after a complete candidate

    return json_strings if json_strings else None


async def main():
    global mcphost
    st.write("🔗 Connecting to MCP servers...")
    server_response=await mcphost.connect_to_servers()
    if server_response["status"]=="STARTED":
        st.write("🔗 Connected to MCP servers...")
        with st.expander("🧩 Registered tools:"): 
            st.write(f"\n {[t['function']['name'] for t in server_response["Tools"]]}")

    with st.container():
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    query=st.chat_input("Enter your query here")
    if query:
        st.chat_message("user").markdown(query)
        st.session_state.chat_messages.append({"role": "user", "content": query})
        assistant_response=None
        with st.chat_message("assistant"):
            with st.spinner("processing",show_time=True):
                ui_action_response = await uiagent_react.run(query)
                ui_action_response=extract_flat_json_strings(str(ui_action_response))
                # st.write("ui_action_response=")
                # st.write(ui_action_response)
                if isinstance(ui_action_response,dict):
                    if ui_action_response.get("action_type")!=None:
                        if ui_action_response["action_type"]=="UI":
                            ui_tool_call(ui_action_response)
                        elif ui_action_response["action_type"]=="CHAT":
                            mcp_tool_response=await mcphost.chat_with_tools(query)
                            st.write(mcp_tool_response)
                            assistant_response=mcp_tool_response
            st.session_state.chat_messages.append({"role": "assistant", "content": assistant_response})
            #display_mcp_response(response)

if __name__ == "__main__":
    asyncio.run(main())
