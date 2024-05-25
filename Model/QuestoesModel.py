from sqlalchemy.orm import relationship
from sqlalchemy import *
import uuid
from datetime import datetime
from Model.Base import Base
from Model.AtividadeModel import questoes_association

def generate_uuid():
    return str(uuid.uuid4())

class QuestaoModel(Base):
    __tablename__ = "questoes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    atividades = relationship("AtividadeModel", secondary=questoes_association, back_populates="questoes")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "atividades": [atividade.to_dict() for atividade in self.atividades]
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
    def update(session, questao):
        with session.begin():
            session.merge(questao)

