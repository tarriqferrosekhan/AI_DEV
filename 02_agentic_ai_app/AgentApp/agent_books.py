import openai
import json
from llama_index.core.tools import FunctionTool
import llama_index.core.agent as llamagent
from llama_index.llms.openai import OpenAI
import os
import openai
import streamlit as st
import asyncio


# --- Streamlit ---
import streamlit as st
openai_api_key=""
openai.api_key=openai_api_key

def RegisterUser()->dict:
    """Register the user"""
    st.session_state.ui_action = "register_user"
    result = {}
    result["ui_action"]="register_user"
    result["msg"]= f"Open registration dialog"
    return result 

@st.dialog("Register user")
def showRegisterUser():
    st.write("show")
    if st.button("close"):
        st.rerun()

UI_PROMPT = f"""
You are the UI of a Policy-Bound Library Assistant.
Follow these exact rules:
- If the user wants to register, call the RegisterUser tool.
"""

UITOOLS = [
    FunctionTool.from_defaults(fn=RegisterUser,description="Register the user",return_direct=True,),
]

llm = OpenAI(model="gpt-4o-mini", temperature=0,api_key=openai_api_key)

uiagent_react = llamagent.FunctionAgent(
    tools=UITOOLS,
    llm=llm,
    verbose=True,
    system_prompt=UI_PROMPT,

)


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Agentic Library Assistant", page_icon="📚")
st.title("📚 Policy-Bound Library Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

if "ui_action" not in st.session_state:
    st.session_state.ui_action = None



async def mainUI():
    query = st.chat_input("Type your request...")
    if query:
        #st.session_state.chat.append(("user", query))
        with st.spinner("processing for '"+query+"'",show_time=True):
            try:
                response = await uiagent_react.run(query)
                if not isinstance(response,dict):
                     response=  json.loads(str(response).replace("'","\""))
                st.write(isinstance(response,dict))
                st.write(str(response))
                if isinstance(response,dict) and response["ui_action"]=="register_user":
                    showRegisterUser()
            except Exception as e:
                    st.write(e)
                    st.session_state.chat.append(("assistant", "Could not process this request. Please retry."))

for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

if __name__ == "__main__":
    os.system('cls')
    asyncio.run(mainUI())
