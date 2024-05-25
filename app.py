from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

import uvicorn

app = FastAPI()

@app.get("/", tags=["Root"])
def return_status():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Welcome to the API!"}

uvicorn.run(app, host="localhost", port=8000)