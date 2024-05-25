from sqlalchemy.orm import relationship
from sqlalchemy import *
import uuid
from datetime import datetime
from Model.Base import Base
from Model.AlunoModel import aluno_atividade_association

def generate_uuid():
    return str(uuid.uuid4())

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
    
    @staticmethod
    def get_by_id(session, id):
        return session.query(AtividadeModel).filter(AtividadeModel.id == id).first()
    
    @staticmethod
    def get_all(session):
        return session.query(AtividadeModel).all()
    
    @staticmethod
    def create(session, atividade):
        with session.begin():
            session.add(atividade)