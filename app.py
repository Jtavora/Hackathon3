from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import subprocess
from Controller.AlunoController import AlunoController
from Model.Base import AlunoModel, AtividadeModel
from Controller.AtividadeController import AtividadeController
from Model.Base import QuestaoModel
from Controller.QuestoesController import QuestoesController

aluno_controller = AlunoController()
atividade_controller = AtividadeController()
questao_controller = QuestoesController()


app = FastAPI()

class Aluno(BaseModel):
    name: str
    email: str
    login: str

class Questao(BaseModel):
    name: str
    gabarito: str
    enunciado: str
    pontuacao: int

class Atividade(BaseModel):
    name: str
    questoes: list[Questao]
    descricao: str


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
    nova_atividade = AtividadeModel(name=atividade.name, descricao=atividade.descricao)
    atividade_controller.cria_atividade(nova_atividade)

    id = atividade_controller.get_atividade_by_name(atividade.name)

    for questao in atividade.questoes:
        nova_questao = QuestaoModel(
            name=questao.name, 
            gabarito=questao.gabarito, 
            enunciado=questao.enunciado, 
            pontuacao=questao.pontuacao, 
            id_atividade=id
        )
        questao_controller.create_questao(nova_questao)

    return {"message": "Atividade created successfully!"}