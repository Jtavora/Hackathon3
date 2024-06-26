import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Table, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload, relationship

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

# Tabela de associação entre alunos e atividades
aluno_atividade_association = Table(
    'aluno_atividade', Base.metadata,
    Column('aluno_id', String(36), ForeignKey('alunos.id')),
    Column('atividade_id', String(36), ForeignKey('atividades.id')),
    UniqueConstraint('aluno_id', 'atividade_id', name='uix_aluno_atividade')
)

class AlunoModel(Base):
    __tablename__ = "alunos"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    login = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    senha = Column(String(100), nullable=False)

    atividades = relationship("AtividadeModel", secondary=aluno_atividade_association, back_populates="alunos")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "login": self.login,
            "created_at": self.created_at,
            "atividades": [atividade.to_dict() for atividade in self.atividades]
        }
    
    @staticmethod
    def get_by_id(session, id):
        return session.query(AlunoModel).filter(AlunoModel.id == id).first()
    
    @staticmethod
    def alunos_list(session):
        return session.query(AlunoModel).all()
    
    @staticmethod
    def create(session, aluno):
        with session.begin():
            session.add(aluno)

    @staticmethod
    def get_by_atividade_id(session, id):
        return session.query(AlunoModel).join(aluno_atividade_association).filter(aluno_atividade_association.c.atividade_id == id).all()
    
    @staticmethod
    def get_aluno_atividades(session, id):
        return session.query(AlunoModel).filter(AlunoModel.id == id).first().atividades
    
    @staticmethod
    def get_login(session, login):
        return session.query(AlunoModel).filter(AlunoModel.login == login).first()

class AtividadeModel(Base):
    __tablename__ = "atividades"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    descricao = Column(String(300))

    questoes = relationship("QuestaoModel", back_populates="atividade")
    alunos = relationship("AlunoModel", secondary=aluno_atividade_association, back_populates="atividades")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "questoes": [questao.to_dict() for questao in self.questoes]
        }

    @staticmethod
    def cria_atividade(session, nome: str, descricao: str = None):
        with session.begin():
            atividade = AtividadeModel(name=nome, descricao=descricao)
            session.add(atividade)
    
    @staticmethod
    def get_atividade_by_name(session, name):
        return session.query(AtividadeModel).filter(AtividadeModel.name == name).first().id
    
    @staticmethod
    def get_all(session):
        return session.query(AtividadeModel).all()
    
    @staticmethod
    def atividades_list(session):
        return session.query(AtividadeModel).options(joinedload(AtividadeModel.questoes)).all()
    
class GrupoAtividadeModel(Base):
    __tablename__="grupo_atividade"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    atividade_id = Column(String(36), ForeignKey('atividades.id'))
    sequencia_pontuacao = Column(Integer, default=0)
    pontuacao = Column(Integer, default=0)

# Tabela de associação entre grupos e alunos
grupo_aluno_association = Table(
    'grupo_aluno', Base.metadata,
    Column('grupo_id', String(36), ForeignKey('grupo_atividade.id')),
    Column('aluno_id', String(36), ForeignKey('alunos.id')),
    UniqueConstraint('grupo_id', 'aluno_id', name='uix_grupo_aluno')
)

from sqlalchemy import Enum


class RespostaAluno(Base):
    __tablename__ = "respostas_aluno"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    resposta = Column(String(300), nullable=False)
    questao_id = Column(String(36), ForeignKey('questoes.id'))
    aluno_id = Column(String(36), ForeignKey('alunos.id'))
    atividade_id = Column(String(36), ForeignKey('atividades.id'))
    status = Column(String(300), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "resposta": self.resposta,
            "status": self.status,
            "questao_id": self.questao_id,
            "aluno_id": self.aluno_id,
            "atividade_id": self.atividade_id
        }
    
    @staticmethod
    def get_by_id(session, id):
        return session.query(RespostaAluno).filter(RespostaAluno.id == id).first()
    
    @staticmethod
    def get_all(session):
        return session.query(RespostaAluno).all()
    
    @staticmethod
    def envia_resposta_aluno(session, resposta):
        with session.begin():
            # Busca a questão
            questao = session.query(QuestaoModel).filter(QuestaoModel.id == resposta.questao_id).first()
            if not questao:
                print("Questão não encontrada.")
                return

            # Busca a atividade relacionada à questão
            atividade_id = questao.id_atividade
            atividade = session.query(AtividadeModel).filter(AtividadeModel.id == resposta.atividade_id).first()
            if not atividade:
                print("Atividade não encontrada.")
                return

            # Busca o grupo do aluno
            grupo_aluno = session.query(grupo_aluno_association).filter(grupo_aluno_association.c.aluno_id == resposta.aluno_id).first()
            if not grupo_aluno:
                print("Grupo não encontrado.")
                return

            # Busca o grupo correspondente ao grupo do aluno
            grupo_id = grupo_aluno.grupo_id
            grupo = session.query(GrupoAtividadeModel).filter(GrupoAtividadeModel.id == grupo_id).first()
            if not grupo:
                print("Grupo não encontrado.")
                return

            # Verifica se a resposta está correta
            if questao.gabarito == resposta.resposta:
                resposta.status = "correta"
                grupo.sequencia_pontuacao += 1
                grupo.pontuacao += questao.pontuacao
            else:
                resposta.status = "incorreta"
                grupo.sequencia_pontuacao = 0

            # Adiciona a resposta do aluno ao banco de dados
            data = RespostaAluno(resposta = resposta.resposta, questao_id = resposta.questao_id, aluno_id = resposta.aluno_id, atividade_id = resposta.atividade_id, status = resposta.status)
            session.add(data)

            return resposta
            # print(resposta)
            # session.add(resposta)
        
class QuestaoModel(Base):
    __tablename__ = "questoes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    gabarito = Column(String(300), nullable=False)
    enunciado = Column(String(300))
    id_atividade = Column(String(36), ForeignKey('atividades.id'))
    pontuacao = Column(Integer, default=1)

    atividade = relationship("AtividadeModel", back_populates="questoes")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "gabarito": self.gabarito,
            "enunciado": self.enunciado,
            "pontuacao": self.pontuacao
        }

    
    @staticmethod
    def get_by_id(session, id):
        return session.query(QuestaoModel).filter(QuestaoModel.id == id).first()
    
    @staticmethod
    def get_all(session):
        return session.query(QuestaoModel).all()
    
    @staticmethod
    def create(session, questao):
        with session.begin():
            session.add(questao)

    @staticmethod
    def get_by_atividade_id(session, id):
        return session.query(QuestaoModel).filter(QuestaoModel.id_atividade == id).all()

            

