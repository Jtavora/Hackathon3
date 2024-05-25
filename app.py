from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
from Controller.AlunoController import AlunoController
from Model.Base import AlunoModel

aluno_controller = AlunoController()

import uvicorn

app = FastAPI()

class Aluno(BaseModel):
    name: str
    email: str
    login: str

@app.get("/", tags=["Root"])
def return_status():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Welcome to the API!"}

@app.post("/alunos/", tags=["Alunos"])
def create_aluno(aluno: Aluno):
    """Cria um novo aluno."""
    client_data = AlunoModel(**aluno.dict())
    aluno_controller.create_aluno(client_data)
    return {"message": "Client created successfully!"}

uvicorn.run(app, host="localhost", port=8000)