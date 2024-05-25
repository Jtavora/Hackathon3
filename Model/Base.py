from sqlalchemy.orm import relationship
from sqlalchemy import *
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

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

    atividades = relationship("AtividadeModel", secondary=aluno_atividade_association, back_populates="alunos")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
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

class AtividadeModel(Base):
    __tablename__ = "atividades"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    questoes = relationship("QuestaoModel", back_populates="atividade")
    alunos = relationship("AlunoModel", secondary=aluno_atividade_association, back_populates="atividades")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "questoes": [questao.to_dict() for questao in self.questoes]
        }

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

class StatusResposta(Enum):
    PENDENTE = "pendente"
    CORRETA = "correta"
    INCORRETA = "incorreta"

from sqlalchemy import Enum

class RespostaAluno(Base):
    __tablename__ = "respostas_aluno"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    resposta = Column(String(300), nullable=False)
    questao_id = Column(String(36), ForeignKey('questoes.id'))
    aluno_id = Column(String(36), ForeignKey('alunos.id'))
    atividade_id = Column(String(36), ForeignKey('atividades.id'))
    status = Column(Enum(StatusResposta), default=StatusResposta.PENDENTE)


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
            "updated_at": self.updated_at,
            "resposta": self.resposta,
            "id_atividade": self.id_atividade
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

    @staticmethod
    def envia_resposta_aluno(session, resposta: str, questao_id: str, aluno_id: str):
        with session.begin():
            # Busca a questão
            questao = session.query(QuestaoModel).filter(QuestaoModel.id == questao_id).first()
            if not questao:
                print("Questão não encontrada.")
                return

            # Busca a atividade relacionada à questão
            atividade_id = questao.id_atividade
            atividade = session.query(AtividadeModel).filter(AtividadeModel.id == atividade_id).first()
            if not atividade:
                print("Atividade não encontrada.")
                return

            # Busca o grupo do aluno
            grupo_aluno = session.query(grupo_aluno_association).filter(grupo_aluno_association.c.aluno_id == aluno_id).first()
            if not grupo_aluno:
                print("Grupo não encontrado.")
                return

            # Busca o grupo correspondente ao grupo do aluno
            grupo_id = grupo_aluno.grupo_id
            grupo = session.query(GrupoAtividadeModel).filter(GrupoAtividadeModel.id == grupo_id).first()
            if not grupo:
                print("Grupo não encontrado.")
                return

            # Cria a resposta do aluno
            resposta_aluno = RespostaAluno(resposta=resposta, questao_id=questao_id, aluno_id=aluno_id, atividade_id=atividade_id)

            # Verifica se a resposta está correta
            if questao.gabarito == resposta:
                resposta_aluno.status = StatusResposta.CORRETA
                grupo.sequencia_pontuacao += 1
                grupo.pontuacao += questao.pontuacao
            else:
                resposta_aluno.status = StatusResposta.INCORRETA
                grupo.sequencia_pontuacao = 0

            # Adiciona a resposta do aluno ao banco de dados
            session.add(resposta_aluno)

