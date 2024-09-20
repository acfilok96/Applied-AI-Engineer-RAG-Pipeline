# RAG Pipeline for Production

## Deployed for Demo Purpose on `Streamlit Cloud` 🔗:

Web Application: **[FlowChat](https://rag-pdf-blu-1-242.streamlit.app/)** 🔗


## `Production Deployment [.py]` Folder

```
Production Deployment [.py]/
      ├── .streamlit/
      │        └── config.toml
      ├── imagefile/
      │        ├── a7.png
      │        └── img33-2.png
      ├── README.md
      ├── avatars.py
      ├── excuses.py
      ├── functions.py
      ├── header.py
      └── requirements.txt
```
  

Download the `Production Deployment [.py]` folder & open it in `Visual Studio Code` or any other IDEs. Open  `terminal` and run there.

## 🛠️ Technology | Tool Stack

At its core, Streamlit uses a client-server model to serve applications, with the Python script acting as the server (backend) and the web browser as the client (frontend).

```
Frontend          :   Streamlit - a python package
Backend           :   Python Script
Frameworks        :   LangChain, LlamaIndex, LlamaParse, HuggingFace
LLMs              :   Llama3-70b through Groq API
Vector Database   :   FAISS [Facebook AI Similarity Search], a free & open-source library for efficient similarity search and clustering of dense vectors.
```

## Set up API Keys 🔗

Change the required API key inside the function of `functions.py` files by generating key accordingly

- **LlamaCloud API key:**  [LlamaCloud](https://cloud.llamaindex.ai/api-key)

- **HuggingFace API key:**  [HuggingFace](https://huggingface.co/settings/tokens)
 
- **Groq API key:**  [groqcloud](https://console.groq.com/keys) 

## How to run on Local System:

-  **Run on terminal:**

-  Install the libraries from `requirements.txt` via. terminal with the command
  
    `> pip install -r requirements.txt`
  
-  Then run the `header.py` file with the command

    `> streamlit run header.py`

    or

   `> python -m streamlit run header.py`
  
-  This command starts the server on `http://localhost:8000` & Open it on web browser and it is ready for use.

## Deploy on Streamlit Cloud:

-  Signup on the [Streamlit Cloud](https://share.streamlit.io/signup) using either GitHub account or using email address.

-  Click on the `Create app` and Attach the GitHub repo link at `Repository` position & root file name `header.py` at `Main file path` position.

![Screenshot (1529)](https://github.com/user-attachments/assets/6525818f-df19-470c-a6e6-b679ea2a1b8e)

## Deployed for Demo Purpose on `Streamlit Cloud` 🔗:

Web Application: **[FlowChat](https://rag-pdf-blu-1-242.streamlit.app/)** 🔗

N.B.: During installation of libraries, the notification Building wheel for `llama-cpp-python (pyproject.toml)` should `done` as it allows to declare which build backend used and which other dependencies are needed to build for project.


