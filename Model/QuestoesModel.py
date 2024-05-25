from sqlalchemy.orm import relationship
from sqlalchemy import *
import uuid
from datetime import datetime
from Model.Base import Base
from AlunoModel import AlunoModel, generate_uuid
from GrupoModel import grupo_aluno_association

class StatusResposta(Enum):
    PENDENTE = "pendente"
    CORRETA = "correta"
    INCORRETA = "incorreta"

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
    def envia_resposta_aluno(session, resposta: String, questao_id: String, aluno_id: String):
        with session.begin():
            questao = session.query(QuestaoModel).filter(QuestaoModel.id == questao_id).first()
            atividade = session.query(QuestaoModel).filter(QuestaoModel.id == questao_id).first().id_atividade
            grupo = session.query(grupo_aluno_association).filter(grupo_aluno_association.c.aluno_id == aluno_id).first().grupo_id
            if questao.gabarito == resposta:
                session.add(RespostaAluno(resposta=resposta, questao_id=questao_id, aluno_id=aluno_id, atividade_id=atividade.id, status='CORRETA'))
                grupo.sequencia_pontuacao += 1
                grupo.pontuacao += questao.pontuacao
            else:
                session.add(RespostaAluno(resposta=resposta, questao_id=questao_id, aluno_id=aluno_id, atividade_id=atividade.id, status='INCORRETA'))
                grupo.sequencia_pontuacao = 0
            

