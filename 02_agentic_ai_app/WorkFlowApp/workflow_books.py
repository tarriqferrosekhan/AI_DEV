import pandas as pd
import os
import openai
import streamlit as st
import asyncio
from llama_index.core.agent import FunctionAgent,ReActAgent
from llama_index.core.tools import FunctionTool

#from llama_index.core.workflow import Workflow, Event, step
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,Context
)
from llama_index.llms.openai import OpenAI

# ---- Define LLM (OpenAI GPT-4o-mini) ----
llm = OpenAI(model="gpt-4o-mini", temperature=0)


# ---- Workflow Definition ----
class LibraryWorkflow(Workflow):

    def __init__(self, timeout = 45, disable_validation = False, verbose = False, service_manager = None, resource_manager = None, num_concurrent_runs = None):
        super().__init__(timeout, disable_validation, verbose, service_manager, resource_manager, num_concurrent_runs=1)
    
    @step()
    async def input_node(self, ev: StartEvent) -> Event:
        """Entry point: receive user query"""
        #st.write("entry point")
        user_msg =ev.to_dict().get("data")["message"]
        return Event(message=user_msg,parent=ev)
    
    @step()
    async def exit_step(self, ev: Event) -> StopEvent:
        """exit step"""
        return StopEvent(message="",parent=ev)

    
    @step()
    async def router(self, ev: Event)->Event:
        text=""
        #st.write(ev.to_dict())
        if ev.to_dict().get("message")!=None:
            text=ev.to_dict().get("message").lower()
        #st.write("router.text="+text)
        substrings_register=["register","signup","sign up","sign-up","subscribe","member"]
        substrings_show=["show","show books","view books","list","what books you have","what all books you have","catalogue"]
        substrings_issue=["issue","take","check out","check-out"]

        if any(sub in text.lower() for sub in substrings_register):
            #st.write("route=register")
            return await self.registration_node(ev) #, payload=ev.to_dict()) #StopEvent(route= "register", parent=ev)
        elif any(sub in text.lower() for sub in substrings_show):
            return await self.viewbooks_node(ev) #, payload=ev.to_dict()) #StopEvent(route= "register", parent=ev)
        elif any(sub in text.lower() for sub in substrings_issue):
            return await self.issue_node(ev) #StopEvent(route= "issue", parent=ev)
        elif "return" in text:
            return await self.return_node(ev) #StopEvent(route= "return", parent=ev)
        else:
            return StopEvent(route= "reply", query= text, parent=ev)


    

    #@step()
    async def registration_node(self, ev: Event) -> StopEvent:
        """Handle registration intent"""
        #st.write("""Handle registration intent""")
        return StopEvent({"ui_action": "show_registration_form", "msg": "Please register"},parent=ev)

    #@step()
    async def issue_node(self, ev: Event) -> StopEvent:
        """book issue"""
        #st.write("""book issue""")
        return StopEvent(
                {"ui_action": "ask_book_name", "msg": "Which book would you like to issue?"}
                ,parent=ev
            )
    
    async def viewbooks_node(self, ev: Event) -> StopEvent:
        """show or view books"""
        #st.write("""book issue""")
        return StopEvent(
                {"ui_action": "show_books", "msg": ""}
                ,parent=ev
            )



    #@step
    async def return_node(self, ev: Event) -> StopEvent:
        """Handle book return intent"""
       
        return StopEvent(
            {"ui_action": "return_book", "msg": "Please return your book at the counter."},
            parent=ev,
        )

    #@step()
    async def reply_node(self, ev: Event) -> StopEvent:
        """General Q&A (policy-based reply from LLM)"""
        query=""
        if ev!=None:
            data = ev.to_dict().get("data")
            print("data",data)
            if data!=None:
                query=data.get("query", "")
            system_prompt = """
            You are the Library Policy Assistant. 
            Only answer questions using the given policies.
            Policies:
            - Membership deposit Rs.1000 individual, Rs.1500 family
            - Fines: Rs.100 for default, Rs.200 for damage
            - Max 2 books per user
            - Return due in 5 days, delays → defaulter
            - Waiting list allowed up to N-3
            - Severe fines for damaging facilities
            """
        reply = llm.complete(system_prompt + f"\nUser: {query}\nAnswer:").text
        return StopEvent({"ui_action": "reply", "content": reply}, parent=ev)

def addSessionStates(key,default_value):
    if key not in st.session_state:
        st.session_state[key]=default_value

def initUISessionStates():
    addSessionStates("show_registration_form",False)
    addSessionStates("registered_users",[])
    addSessionStates("chat_history",[])

initUISessionStates()

def addChatHistory(role,content):
    st.session_state["chat_history"].append({"role": role, "content": content})

@st.dialog("Registration")
def showRegistrationDialog():
    st.markdown("### Register New Member")
    with st.form("registratoin",enter_to_submit=False,clear_on_submit=True):
        name = st.text_input("Name", key="reg_name")
        membership_type = st.selectbox("Membership Type", ["Individual", "Family"], key="reg_type")
        submitted = st.form_submit_button("Submit")
        # Handle submission
        if submitted:
            st.session_state.registered_users.append({"name": name, "type": membership_type})
            addChatHistory("assistant", f"✅ Registered {name} as {membership_type} member!")
            st.rerun()

def showRegisteredUsers():
    if st.session_state.registered_users:
        st.markdown("### Registered Users")
        for u in st.session_state.registered_users:
            st.write(f"{u['name']} ({u['type']})")


def spellcheck(sentence,openai_api_key):
    client = openai.OpenAI(api_key=openai_api_key)
    #sentence = "He go to library yesterday and forgot bring his book."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a grammar and style corrector."},
            {"role": "user", "content": f"Correct this sentence: {sentence}"}
        ]
    )

    return response.choices[0].message.content

@st.dialog("Show the Books")
def showBooks():
    base_path = os.getcwd()+"\\"
    path_books=base_path+"books_gpt.csv"
    df=pd.read_csv(path_books)
    st.write(df)

def issueBooks():
    base_path = os.getcwd()+"\\"
    path_books=base_path+"books_gpt.csv"
    df=pd.read_csv(path_books)
    st.write(df)

async def mainUI():
# ---- Streamlit App ----
    st.title("📚 Agentic Library (Workflow + OpenAI)")
    user_input = st.chat_input("Ask the library agent...")
    if user_input:
        # Run workflow
        wf = LibraryWorkflow()
        addChatHistory("user", user_input)
        response = await wf.run(data={"message":spellcheck(user_input,openai_api_key)})

        if isinstance(response, dict) and response.get("ui_action") == "show_registration_form":
            showRegistrationDialog()
        elif isinstance(response, dict) and response.get("ui_action") == "show_books":
            showBooks()
        elif isinstance(response, dict) and response.get("ui_action") == "ask_book_name":
            st.chat_message("assistant").write(response["msg"])
            # You can extend with st.text_input for book name
        elif isinstance(response, dict) and response.get("ui_action") == "return_book":
            st.chat_message("assistant").write(response["msg"])
        elif isinstance(response, dict) and response.get("ui_action") == "reply":
            st.chat_message("assistant").write(response["content"])

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if __name__ == "__main__":
    os.system('cls')
    asyncio.run(mainUI())
