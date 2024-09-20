'''Install all the required libraries'''

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
            LLAMA_PARSE_API_KEY = str("Enter your LlamaParse API key here")
        
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
           
            print(llama_parse_documents)
            
            parsed_doc = llama_parse_documents[0]
            print(parsed_doc)
        
            loaded_documents = Document(page_content = parsed_doc.text,
                                        metadata = {"source" : "This is a PDF Document about information."})
            loaded_documents = [loaded_documents]
        
            text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 400)
            docs = text_splitter.split_documents(loaded_documents)
            return docs
                
        except Exception as e:
            return None
            
            
    @staticmethod
    def DocDatabase(docs):
        '''
        The data is converted into vector form using an embedding model, making it understandable for computers. For this project, FastEmbedEmbeddings model have been used.
        These vector embeddings are saved in a vector database, allowing them to be easily searched. FAISS [Facebook AI Similarity Search], a free & open-source library for efficient similarity search and clustering of dense vectors.
        '''
        try:
            HF_TOKEN = str("Enter your HuggingFace API key here")
            embeddings = FastEmbedEmbeddings(model_name = "BAAI/bge-base-en-v1.5")
        
            database = FAISS.from_documents(docs, embeddings)
            return database
        
        except Exception as e:
            return None


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
            return None


    @staticmethod   
    def DocModel():
        '''
        Setting up the base LLM, Llama3-70b model via. Groq for the retrieval process with ground instruction as system prompt for LLM.
        '''
        try:
            GROQ_API_KEY = str("Enter Your Groq API key here")
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
            return None


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
            return None


    @staticmethod    
    def DocSystemPrompt():
        ''' 
        Instruction about document for llama-parse during document parsing process.
        '''
        try:
            system_prompt = f"""Try to be precise while answering the questions."""
            return system_prompt
        
        except Exception as e:
            return None



    @staticmethod   
    def DocResponseGeneration(qa, user_prompt):
        '''
        Here we fetching the retriever with a query and we are getting expected response.
        ''''
        try:
            response = qa.invoke(str(user_prompt))
            return response
        
        except Exception as e:
            return None
        

    @staticmethod   
    def ChatPDFFunction(pdf_file, user_prompt):
        ''' 
        Combine Chatbot Function: All parts have been combined here for developing a RAG pipeline
        ''''
        try:
            system_prompt = Functions.DocSystemPrompt()

            docs = Functions.DocSpliting(pdf_file, system_prompt)
            database = Functions.DocDatabase(docs)
            
            compression_retriever = Functions.DocRetriever(database)
            [llm, model_prompt] = Functions.DocModel()
            
            qa = Functions.DocRetrievalQA(llm, model_prompt, compression_retriever)
            
            query_result = Functions.DocResponseGeneration(qa, user_prompt)
            
            return query_result["result"]
        except Exception as e:
            return None
                        
