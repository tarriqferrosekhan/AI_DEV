import streamlit as st
from Utils import Utils
from BooksRAG import BooksRAG
from AppMessage import MessageType

def initialize_conversation():
  st.set_page_config(page_title="HelpMateAI.Books (RAG)")
  st.info ("Welcome to BookBot! Ask me for book recommendations." )
  with st.expander("View Instructions"):  
    st.markdown("""
    <p style="text-align: justify;">
    <ul>
    <li>You are Interacting with an AI system that will be help you to fetch books from specific catalogue and return <b>top n</b> matches.<br></li>
    <li>For Faster and better results please ensure to include these attributes (Genre,Published Year, Pages Count,Price) in your prompt.<br></li>
    <li><b>Any query out of scope of the Books Catalogue will not be served</b></li>
    <li><b>Any unwarranted questions that endangers the society/ unethical etc,.will not be answered by the Bot</b></li>
    </ul>
    </p>
    """, unsafe_allow_html=True)
  with st.expander("View Example Prompts"):
    st.markdown("""
    <ul>
    <li>Can you recommend a Physics book</li>
    <li>Can you recommend a book for research</li>
    <li>Can you recommend a book of price say 1000 INR</li>
    <li>Can you recommend a book on Physics of price around 1500 INR</li>
    <li>Can you recommend a book on Physics of price around 1500 INR and of 450 pages</li>
    <li>Can you recommend a book on Physics of price around 1500 INR and of 450 pages published within 5 years</li>
    </ul>""",unsafe_allow_html=True)

def showProductRecommendation(filtered_df):
    if filtered_df.empty==False:
        with st.expander("View /Download Result: ["+str(filtered_df.shape[0])+" record(s)] "):
            st.write(filtered_df)
    else:
        st.warning("No Data Found!")

def displayMessage(message,message_type:MessageType=MessageType.Simple):
    if message_type==MessageType.Simple:
        st.write(message)
    elif message_type==MessageType.Info:
        st.info(message)
    elif message_type==MessageType.Warnings:
        st.warning(message)
    elif message_type==MessageType.Error:
        st.error(message)

def main():
    initialize_conversation()
    booksrag=BooksRAG()
    with st.sidebar:
        st.download_button(label="Download Data Source",data=booksrag.path_books,file_name="data.csv",mime="text/csv",icon=":material/download:")
    query=st.chat_input(Utils.Messages.Chat_Input_PlaceHolder)
    if query=="" or query==None:
        return
    if len(query.split(" "))<3:
        displayMessage(Utils.Messages.AtLeastWords,MessageType.Error)
        return
    with st.spinner(Utils.Messages.Spinner,show_time=True):
        _appMessage=booksrag.process(query)
        if _appMessage.Message_Type!=MessageType.Success:
            displayMessage(_appMessage.Response_Message,_appMessage.Message_Type)
        if _appMessage.Message_Type==MessageType.Success:
            showProductRecommendation(_appMessage.Data)
main()