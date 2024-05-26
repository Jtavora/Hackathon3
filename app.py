import subprocess

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from Controller.AlunoController import AlunoController
from Controller.AtividadeController import AtividadeController
from Controller.QuestoesController import QuestoesController
from Controller.RespostaController import RespostaController
from Model.Base import AlunoModel, AtividadeModel, QuestaoModel

aluno_controller = AlunoController()
atividade_controller = AtividadeController()
questao_controller = QuestoesController()
resposta_controller = RespostaController()



app = FastAPI()

class Aluno(BaseModel):
    name: str
    email: str
    login: str
    senha: str

class Questao(BaseModel):
    name: str
    gabarito: str
    enunciado: str
    pontuacao: int

class Atividade(BaseModel):
    name: str
    questoes: list[Questao]
    descricao: str

class Login(BaseModel):
    login: str
    senha: str

class Resposta(BaseModel):
    resposta : str
    questao_id : str
    aluno_id : str
    atividade_id : str
    status : str = "pendente"



@app.get("/", tags=["Root"])
def return_status():
    """Retorna uma mensagem de boas-vindas."""
    return {"message": "Welcome to the API!"}

@app.post("/login/", tags=["Alunos"])
def login(login: Login):
    """Realiza o login de um aluno."""
    aluno = aluno_controller.get_login(login.login)
    if aluno.senha == login.senha:
        return {"id": aluno.id}
    else:
        return {"message": "Login failed!"}

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

@app.get("/atividades/", tags=["Atividades"])
def get_atividades_and_questoes():
    atividades = atividade_controller.get_atividades_and_questoes_list()
    return {"atividades": [atividade.to_dict() for atividade in atividades]}

@app.post("/resposta/", tags=["Resposta"])
def enviar_resposta(resposta: Resposta):
    resposta_data = Resposta(**resposta.dict())
    retorno = resposta_controller.enviar_resposta(resposta_data)
    if retorno != None:
        return {"message": "Resposta enviada com sucesso!", "questao": retorno}
    return {"message": "Erro ao enviar resposta"}