import streamlit as st
from excuses import Excuses
 
import nest_asyncio
nest_asyncio.apply()

import os, tempfile

from langchain.schema import Document 
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from llama_parse import LlamaParse

from langchain.retrievers import ContextualCompressionRetriever

from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from streamlit_chat import message
from avatars import Avatar

import nltk
nltk.download('wordnet')


class Functions:
    '''
    `Functions` class is a combination of the RAG pipeline with multiple required functions.
    '''
    def __init__(self):
        pass

    @staticmethod
    def DocSpliting(pdf_file, system_prompt):
        '''
        This function is used to parse the document information using the llamaparse library.
        LlamaParse is a GenAI-native document parser that can parse complex document data for any downstream LLM use case (RAG, agents).
        '''
        try:
            LLAMA_PARSE_API_KEY = str("Enter Llama Parse API key here")
        
            instruction = system_prompt
        
            parser = LlamaParse(
                                api_key = LLAMA_PARSE_API_KEY,
                                result_type = "markdown",
                                parsing_instruction = instruction,
                                max_timeout = 5000,
                            )
            
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, pdf_file.name)
            with open(path, "wb") as f:
                f.write(pdf_file.getvalue())
                
            llama_parse_documents = parser.load_data(path)
            parsed_doc = llama_parse_documents[0]
        
            loaded_documents = Document(page_content = parsed_doc.text,
                                        metadata = {"source" : "A delivery chalan or invoice."})
            loaded_documents = [loaded_documents]
        
            text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 400)
            docs = text_splitter.split_documents(loaded_documents)
            return docs
                
        except Exception as e:
            st.warning("Upload Document or Corrupted Document!")
            # return None
            
            
    @staticmethod
    def DocDatabase(docs):
        '''
        The data is converted into vector form using an embedding model, making it understandable for computers. For this project, FastEmbedEmbeddings model have been used.
        These vector embeddings are saved in a vector database, allowing them to be easily searched. FAISS [Facebook AI Similarity Search], a free & open-source library for efficient similarity search and clustering of dense vectors.
        '''
        try:
            HF_TOKEN = str("Enter Hugging Face API key here")
            embeddings = FastEmbedEmbeddings(model_name = "BAAI/bge-base-en-v1.5")
        
            database = FAISS.from_documents(docs, embeddings)
            return database
        
        except Exception as e:
            st.warning("Upload Document or Corrupted Document!")
            # return None


    @staticmethod
    def DocRetriever(database):
        '''
        Here is the retriever technique with a maximum top 5 similar phrases with user query would be fetch.
        '''
        try:
            retriever = database.as_retriever(search_kwargs = {"k" : 5})
        
            # compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2")
            # compression_retriever = ContextualCompressionRetriever(
            #     base_compressor = compressor, base_retriever = retriever)
            return retriever # compression_retriever
        
        except Exception as e:
            st.warning("Upload Document or Corrupted Document!")
            # return None


    @staticmethod   
    def DocModel():
        '''
        Setting up the base LLM, Llama3-70b model via. Groq for the retrieval process with ground instruction as system prompt for LLM.
        '''
        try:
            GROQ_API_KEY = str("Enter Groq API key here")
            llm = ChatGroq(temperature = 0,
                            model_name = "llama3-70b-8192",
                            groq_api_key = GROQ_API_KEY,
                            max_tokens = 3024)
        
            prompt_template = """
            
            Use the following pieces of information to answer the user's question.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
            Context: {context}
            Question: {question}
        
            Answer the question and provide additional helpful information,
            based on the pieces of information, if applicable. Be succinct.
        
            Responses should be properly formatted to be easily read.
            
            """
        
            prompt = PromptTemplate(template = prompt_template,
                                    input_variables = ["context", "question"])
            
            return [llm, prompt]
        
        except Exception as e:
            st.warning("Upload Document or Corrupted Document!!")
            # return None


    @staticmethod   
    def DocRetrievalQA(llm, prompt, compression_retriever):
        '''
        Combining all the parts i.e. LLM, retriever, system prompt for generating response for user's query.
        '''
        try:
            qa = RetrievalQA.from_chain_type(
                        llm = llm,
                        chain_type = "stuff",
                        retriever = compression_retriever,
                        return_source_documents = True,
                        chain_type_kwargs = {"prompt" : prompt, "verbose" : False},
                    )
            return qa
        
        except Exception as e:
            st.warning("Upload Document or Corrupted Document!")
            # return None


    @staticmethod    
    def DocSystemPrompt():
        ''' 
        Instruction about document for llama-parse during document parsing process.
        '''
        try:
            show_advanced_info_0 = st.sidebar.toggle(":blue[**Further Instruction**]", value = False)
            system_prompt = f"""Try to be precise while answering the questions."""
            system_prompt_temp = f"""\n"""
            if show_advanced_info_0:
                system_prompt_temp = st.sidebar.text_input(":blue[**Additional Instruction About Document**]", placeholder = "Enter here", help = "For example, The provided document is Meta First Quarter 2024 Results. \
                This form provides detailed financial information about the company's performance for a specific quarter. \
                It includes unaudited financial statements, management discussion and analysis, and other relevant disclosures required by the SEC. \
                It contains many tables.")
                system_prompt = str(system_prompt) + str("\n\n") + str(system_prompt_temp)
            return system_prompt
        
        except Exception as e:
            st.warning("Upload Document or Corrupted Document!")
            # return None


    @staticmethod    
    def DocLoadData():
        '''
        Loading the document.
        '''
        try:
            with st.sidebar:
                st.header("**Upload Document**")
                pdf_file = st.file_uploader("Upload PDF file", type = ["pdf"], accept_multiple_files = False) 
                if pdf_file:
                    st.sidebar.info("Document Uploaded !")
            return pdf_file
        
        except Exception as e:
            st.warning("Upload Document or Corrupted Document!")
            # return None


    @staticmethod   
    def DocResponseGeneration(qa, user_prompt):
        '''
        Here we fetching the retriever with a query and we are getting expected response.
        ''''
        # with st.spinner(":green[Typing . . . ]"):
        try:
            response = qa.invoke(str(user_prompt))
            return response
        
        except Exception as e:
            st.warning("Upload Document or Corrupted Document!")
            # return None


    @staticmethod       
    def DocShowResponse(response, user_prompt):
        '''
        Show the response for given query.
        '''
        try:
            do1, do2 = st.columns((0.5, 3.5))
            with do1:
                st.info(str("**Query:**"))
            with do2:
                st.info(user_prompt)
            col1, col2 = st.columns((2.5, 1.5))
            with col1:
                st.warning("**Response:**")
            with col1.container(height = 550, border = False):
                st.info(response["result"])
            with col2:
                st.warning("**Supported Documents:**")
            with col2.container(height = 550, border = False):
                for i, doc in enumerate(response["source_documents"]):
                    st.info(str("**Document**")+str("\t\t")+str(i+1)+str("\t\t")+str("**:**"))
                    st.markdown(str(doc.page_content))
                    st.write("--------------------------------")
        except Exception as e:
            st.write("Ask once again @ DocShowResponse !")
        
            
    @staticmethod
    def DocShowAppInfo():
        '''
        About application details.
        '''
        show_info_1 = st.sidebar.toggle(":blue[*Application Details*]", value = False)
        if show_info_1:
            st.sidebar.info("""

                        **ChatPDF Application**

                        - **Details:** 
                        1. *LlamaIndex* for orchestration
                        2. *Streamlit* for creating a Chat UI
                        3. *Meta AI's Llama3* as the LLM
                        4. *"BAAI/bge-base-en-v1.5"* for embedding generation
                        
                        - **Language:** *English*
                        
                        - **Release Date:** *June, 2024*
                        
                        """)
            
        show_info_2 = st.sidebar.toggle(":blue[*Developer Details*]", value = True)
        if show_info_2:
            st.sidebar.info("""
                        
                        :rainbow[**This application has been created by [:blue[Dipankar Porey]](https://www.linkedin.com/in/dipankar-porey-403320259/),
                        BluWebMedia IT Services Pvt. Ltd, Ernst & Young.**] 
                        
                        """)

    @staticmethod
    def ChatBot():
        ''' 
        Combine Chatbot Function: All parts have been combined here for developing a RAG pipeline and this is also the design of frontend of streamlit application.
        '''

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
        
        with st.sidebar:
            st.session_state.system_prompt = Functions.DocSystemPrompt()
            st.write("Hello")
            st.header("**Document**")
            pdf_file = st.file_uploader("Upload PDF file", type = ["pdf"], accept_multiple_files = False)
            if pdf_file:
                with st.spinner(":blue[Loading . . .]"):
                    st.session_state.docs = Functions.DocSpliting(pdf_file, st.session_state.system_prompt)
                    st.session_state.database = Functions.DocDatabase(st.session_state.docs)
                    st.session_state.compression_retriever = Functions.DocRetriever(st.session_state.database)
                    [st.session_state.llm, st.session_state.prompt] = Functions.DocModel()
                    st.session_state.qa = Functions.DocRetrievalQA(st.session_state.llm, st.session_state.prompt, st.session_state.compression_retriever)
                    st.sidebar.info("Document Uploaded !")
            
        
        if "messages_show" not in st.session_state:
            st.session_state.messages_show = []
        
        k = 1
        for message_s in st.session_state.messages_show:
            if message_s["role"] == "user":
                avatar_style = str(Avatar.listofAvatar())
                message(message_s["content"], is_user = True, key = str(k) + '_user', avatar_style = avatar_style, seed = "user")
            elif message_s["role"] == "assistant":
                avatar_style = str(Avatar.listofAvatar())
                message(message_s["content"], key = str(k), avatar_style = avatar_style, seed = "assistant", allow_html = True)
            k += 1

        def clear_chat_history():
            st.session_state.messages_show = []
            
            
        col1, col2 = st.sidebar.columns((0.35,1.75))
        with col2:
            st.button(':green[*New Chat*]', on_click = clear_chat_history)

        Functions.DocShowAppInfo()
        
        if prompt := st.chat_input("Ask me here 😊!"):
            
            st.session_state.messages_show.append({"role": "user", "content": prompt})
            
            avatar_style = str(Avatar.listofAvatar()) 
            message(prompt, is_user = True, key = str(k) + '_user', avatar_style = avatar_style, seed = "user")

            k += 1
            with st.spinner(":blue[Typing . . .]"): 
                try:
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
            st.info("""

            Introducing the RAG application for PDF document. Upload PDF file and search \
            queries to find information within document.
            
            **About RAG :** This is a sophisticated RAG model capable of extracting tabular patterns from complex PDF documents in text format for advanced question answering.

            """)
            # st.warning("👈 Upload required document and continue question answering conversation with document !")
            st.warning("""

            In *Additional Instruction About Document*, it can be put about document and instruction for question answering performance.
            
            By default, \
            It is set to *Try to be precise while answering the questions.*
            
            For example, Instruction can be given for a invoice or challan document \
            as *The provided document is a delivery chalan or invoice. \
                This form provides detailed chalan or invoice information about the company's performance for a specific quarter. \
                It includes unaudited invoice statements, management discussion and analysis, and other relevant disclosures required by the SEC. \
                It contains many tables.*

            """)
