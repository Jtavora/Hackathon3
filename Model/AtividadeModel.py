from sqlalchemy.orm import relationship
from sqlalchemy import *
import uuid
from datetime import datetime
from Model.Base import Base
from Model.AlunoModel import aluno_atividade_association, generate_uuid


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