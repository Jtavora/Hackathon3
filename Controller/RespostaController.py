import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Model.Base import RespostaAluno

load_dotenv()

database_url = os.getenv('DATABASE_URL')

class RespostaController:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_resposta_by_id(self, id):
        with self.Session() as session:
            resposta = RespostaAluno.get_by_id(session, id)
        return resposta

    def get_respostas_list(self):
        with self.Session() as session:
            respostas = RespostaAluno.get_all(session)
        return respostas
    
    def create_resposta(self, resposta):
        with self.Session() as session:
            RespostaAluno.create(session, resposta)
    
    def get_by_atividade_id(self, id):
        with self.Session() as session:
            respostas = RespostaAluno.get_by_atividade_id(session, id)
        return respostas
    
    def enviar_resposta(self, resposta):
        with self.Session() as session:
            resposta = RespostaAluno.envia_resposta_aluno(session, resposta)
            return resposta
