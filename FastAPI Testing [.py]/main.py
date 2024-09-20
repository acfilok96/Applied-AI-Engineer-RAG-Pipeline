from fastapi import FastAPI, HTTPException
from functions import Functions

# FastAPI instance
app = FastAPI()

pdf_file = "meta-earnings.pdf"

# API endpoint to fetch response for user query
@app.get("/{user_query}", response_model=dict)
async def chatWithPDF(user_query: str) -> str:
    response = Functions.ChatPDFFunction(pdf_file, user_query)
    if response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return {"Query\n": user_query, "\nResponse\n": response}