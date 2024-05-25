from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import subprocess
from Controller.AlunoController import AlunoController
from Model.Base import AlunoModel, AtividadeModel

aluno_controller = AlunoController()


app = FastAPI()

class Aluno(BaseModel):
    name: str
    email: str
    login: str

class Questao(BaseModel):
    name: str
    gabarito: str
    enunciado: str
    id_atividade: str
    pontuacao: int

class Atividade(BaseModel):
    name: str
    descricao: str
    questoes: list['Questao']



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


@app.post("/atividades/", tags=["Atividades"])
def post_atividade(atividade: Atividade):
    retorno = AtividadeModel.cria_atividade(atividade.name, atividade.questoes, atividade.descricao)
    if retorno is None:
        raise HTTPException(status_code=400, detail="Falha ao criar atividade")
    return JSONResponse(status_code=201, content=retorno)
