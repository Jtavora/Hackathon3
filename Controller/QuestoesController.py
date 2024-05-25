from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model.Base import QuestaoModel, GrupoAtividadeModel
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv('DATABASE_URL')

class QuestoesController:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_questao_by_id(self, id):
        with self.Session() as session:
            questao = QuestaoModel.get_by_id(session, id)
        return questao

    def get_questoes_list(self):
        with self.Session() as session:
            questoes = QuestaoModel.get_all(session)
        return questoes
    
    def create_questao(self, questao):
        with self.Session() as session:
            QuestaoModel.create(session, questao)
    
    def get_by_atividade_id(self, id):
        with self.Session() as session:
            questoes = QuestaoModel.get_by_atividade_id(session, id)
        return questoes
    
    def enviar_resposta(self, id, resposta):
        with self.Session() as session:
            questao = QuestaoModel.get_by_id(session, id)
            questao.resposta = resposta
            session.commit()
        return questao
    
    def get_pontuacao_grupo(self, usuario_id, atividade_id):
        with self.Session() as session:
            pontuacao = GrupoAtividadeModel.retorna_pontuacao(session, usuario_id, atividade_id)