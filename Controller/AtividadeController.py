from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model.Base import AtividadeModel
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv('DATABASE_URL')

class AtividadeController:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def cria_atividade(self, atividade):
        with self.Session() as session:
            AtividadeModel.cria_atividade(session, atividade.name, atividade.descricao)
    
    def get_atividade_by_name(self, name):
        with self.Session() as session:
            id = AtividadeModel.get_atividade_by_name(session, name)
        return id

    def get_atividades_and_questoes_list(self):
        with self.Session() as session:
            atividades = AtividadeModel.atividades_list(session)
        return atividades