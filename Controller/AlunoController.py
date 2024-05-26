import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Model.Base import AlunoModel, aluno_atividade_association

load_dotenv()


database_url = os.getenv('DATABASE_URL')

class AlunoController:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_aluno_by_id(self, id):
        with self.Session() as session:
            aluno = AlunoModel.get_by_id(session, id)
        return aluno
    
    def get_alunos_list(self):
        with self.Session() as session:
            alunos = AlunoModel.alunos_list(session)
        return alunos
    
    def create_aluno(self, aluno):
        with self.Session() as session:
            AlunoModel.create(session, aluno)
        
    def get_by_atividade_id(self, id):
        with self.Session() as session:
            alunos = AlunoModel.get_by_atividade_id(session, id)
        return alunos
    
    def get_aluno_atividades(self, id):
        with self.Session() as session:
            atividades = AlunoModel.get_aluno_atividades(session, id)
        return atividades
    
    def get_login(self, login):
        with self.Session() as session:
            aluno = AlunoModel.get_login(session, login)
        return aluno