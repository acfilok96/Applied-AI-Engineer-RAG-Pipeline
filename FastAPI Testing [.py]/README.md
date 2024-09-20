# FastAPI Testing for the application

## `FastAPI Testing [.py]` Folder
```
FastAPI Testing [.py]/
      |
      ├── 12587973.pdf
      ├── functions.py
      ├── main.py
      ├── README.md
      └── requirements.txt
```
  

Download the `FastAPI Testing [.py]` folder & open it in `Visual Studio Code` or any other IDEs. Open  `terminal` and run there.

## Set up API Keys 🔗

Change the required API key inside the function of `functions.py` files by generating key accordingly

- **LlamaCloud API key:**  [LlamaCloud](https://cloud.llamaindex.ai/api-key)

- **HuggingFace API key:**  [HuggingFace](https://huggingface.co/settings/tokens)
 
- **Groq API key:**  [groqcloud](https://console.groq.com/keys) 

## How to run:

-  **Run on terminal:**

-  Install the libraries from `requirements.txt` via. terminal with the code
  
     `> pip install -r requirements.txt`
  
-  Then run the `main.py` file with the code

     `> uvicorn main:app --reload`
  
-  run the FastAPI server using: `uvicorn main:app --reload` where filename is `main.py` 
-  Replace main with your script name if different. This command starts the server on http://127.0.0.1:8000.

## Accessing the FastAPI:
-  Open a web browser or use tools like curl or Postman.
-  Navigate to `http://127.0.0.1:8000/{user_query}`, where `{user_query}` is the query you want to retrieve the answer for.
-  Example: `http://127.0.0.1:8000/Tell about meta's early income.` & this will return user's query and response i.e.

    ```
    Query: 
    Tell about Operations Sales Manager role.
    ```
    

    ```
     Response: Operations Sales Manager Role

     As an Operations Sales Manager, I was responsible for establishing operational objectives and work plans, delegating assignments to subordinate managers, and supervising a team of 15 area managers and 35 associates. My key responsibilities included:

     Developing executive presentations and reports to facilitate project evaluation and process improvement
     Directing planning, budgeting, vendor selection, and quality assurance efforts
     Defining clear targets and objectives and communicating them to other team members
     Reviewing sales, customer concerns, and new opportunities to drive business strategy at weekly planning sessions
     Assessing vendor products and maintaining positive vendor relations
     Supporting the sales team in writing proposals and closing contracts
     Developing quarterly and annual sales department budgets
     Developing a comprehensive training program for new sales associates
     Reviewing operational records and reports to project sales and determine profitability
     Training all incoming sales team members
     Maintaining knowledge of current sales and promotions, policies regarding payment and exchanges, and security practices.
     This role allowed me to utilize my skills in leadership, communication, and sales strategy to drive business growth and achieve sales targets.
    ```
