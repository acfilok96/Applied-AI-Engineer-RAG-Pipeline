import streamlit as st
from functions import *


st.set_page_config(page_title = 'FlowChat', layout = "wide", page_icon = "imagefile/a7.png", initial_sidebar_state = 'collapsed')

def details():
    st.sidebar.success("""
                    
                    :green[**This application has been created by [:blue[Dipankar Porey]](https://www.linkedin.com/in/dipankar-porey-403320259/),
                    BluWebMedia Pvt. Ltd., Ernst & Young.**]
                    
                    """)

st.markdown("""
<style>
.big-font-1 {
    font-size:30px !important;
    text-align: center; 
    color: yellow;
    font-weight: 300;
    font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
    background-color: #09090C;
    border-radius: 8px;
    padding: 3px;
}
</style>
""", unsafe_allow_html = True)

# 1EEC4A

st.markdown("""
<style>
.big-font-2 {
    font-size:17px !important;
    text-align: center; 
    color: yellow;
    background-color: #32323B;
    border-radius: 10px;
    padding: 7px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.big-font-3 {
    font-size:17px !important;
    text-align: center; 
    color: yellow;
    background-color: #304F81;
    border-radius: 5px;
    padding: 7px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.big-font-4 {
    font-size:15px !important;
    text-align: center; 
    color: yellow;
    background-color: #304F81;
    border-radius: 4px;
    padding: 3px;
}
</style>
""", unsafe_allow_html=True)


'''
Combine Chatbot Function: All parts have been combined here for developing a RAG pipeline and this is also the design of frontend of streamlit application.
'''

## Sidebar details
st.sidebar.image("imagefile/img33-2.png")
st.sidebar.info("""

:blue[**Welcome to FlowChat**] \n

""")

st.sidebar.markdown('<p class="big-font-2">FlowChat : PDF Q&A</p>', unsafe_allow_html=True)
st.markdown('<p class = "big-font-1">FlowChat</p>', unsafe_allow_html = True)

## Container details 
container_deck = st.container(height = 350, border = False)

## Load as a local system 
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = None
if "docs" not in st.session_state:
    st.session_state.docs = None
if "database" not in st.session_state:
    st.session_state.database = None
if "compression_retriever" not in st.session_state:
    st.session_state.compression_retriever = None
if "llm" not in st.session_state:
    st.session_state.llm = None
if "prompt" not in st.session_state:
    st.session_state.prompt = None
if "qa" not in st.session_state:
    st.session_state.qa = None

## File upload 
with st.sidebar:
    st.session_state.system_prompt = Functions.DocSystemPrompt()
    pdf_file = st.file_uploader(":blue[**Upload PDF file**]", type = ["pdf"], accept_multiple_files = False) 
    if pdf_file:
        st.markdown('<p class="big-font-4">Document Uploaded !</p>', unsafe_allow_html=True)
    
## Temporary Chat-memory
if "messages_show" not in st.session_state:
    st.session_state.messages_show = []

def clear_chat_history():
    st.session_state.messages_show = []
    
col1, col2 = st.sidebar.columns((0.35,1.75))
with col2:
    st.button(':blue[**New Chat**]', on_click = clear_chat_history)


## Temporary Chat-memory Scroll-bar
with container_deck:
    k = 1
    for message_s in st.session_state.messages_show:
        if message_s["role"] == "user":
            avatar_style = str(Avatar.listofAvatar())
            message(message_s["content"], is_user = True, key = str(k) + '_user', avatar_style = avatar_style, seed = "user")
        elif message_s["role"] == "assistant":
            avatar_style = str(Avatar.listofAvatar())
            message(message_s["content"], key = str(k), avatar_style = avatar_style, seed = "assistant", allow_html = True)
        k += 1


## About 
st.sidebar.markdown('<p class="big-font-2">About</p>', unsafe_allow_html=True)
details()

## Conversation Part
if prompt := st.chat_input("Ask me here 😊!"):

    with container_deck:
        st.session_state.messages_show.append({"role": "user", "content": prompt})
        
        avatar_style = str(Avatar.listofAvatar()) 
        message(prompt, is_user = True, key = str(k) + '_user', avatar_style = avatar_style, seed = "user")
    
        k += 1
        with st.spinner(":blue[Typing . . .]"): 
            try:
                st.session_state.docs = Functions.DocSpliting(pdf_file, st.session_state.system_prompt)
                st.session_state.database = Functions.DocDatabase(st.session_state.docs)
                st.session_state.compression_retriever = Functions.DocRetriever(st.session_state.database)
                [st.session_state.llm, st.session_state.prompt] = Functions.DocModel()
                st.session_state.qa = Functions.DocRetrievalQA(st.session_state.llm, st.session_state.prompt, st.session_state.compression_retriever)
                query_result = Functions.DocResponseGeneration(st.session_state.qa, prompt)
                response = query_result["result"]
                avatar_style = str(Avatar.listofAvatar())
                message(response , key = str(k), avatar_style = avatar_style, seed = "assistant", allow_html=True)
            except Exception as e:
                response = Excuses.listofExcuses()
                avatar_style = str(Avatar.listofAvatar()) 
                message(response, key = str(k), avatar_style = avatar_style, seed = "assistant", allow_html=True)
            
        st.session_state.messages_show.append({"role": "assistant", "content": response})
else:
    with container_deck:
        if pdf_file:
            st.markdown('<p class="big-font-3">Document uploaded & Continue Q&A . . . !</p>', unsafe_allow_html=True)
        else:
            st.warning("""
    
            **Introducing :blue[FlowChat] to do Q&A with PDF document. :blue[FlowChat] is capable of extracting tabular patterns from document for advanced Q&A.**
    
            """)
            st.success("👈 **Upload relevant document at the :green[sidebar] and continue question answering conversation with document !**")
            st.info("""
    
            **In :green[Further Instruction], it can be put about document and instructions for question answering performance.**
            
            **By default, It is set to :blue['Try to be precise while answering the questions.']**
            
            **For example, :green[Further Instruction] can be given for a invoice or challan document** \
            **as :blue['The provided document is a delivery chalan or invoice. \
            This form provides detailed chalan or invoice information about the company's performance for a specific quarter.']**
    
            """)
