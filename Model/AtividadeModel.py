from sqlalchemy.orm import relationship
from sqlalchemy import *
import uuid
from datetime import datetime
from Model.Base import Base

def generate_uuid():
    return str(uuid.uuid4())

questoes_association = Table('questoes_association', Base.metadata,
    Column('atividade_id', String(36), ForeignKey('atividades.id')),
    Column('questao_id', String(36), ForeignKey('questoes.id'))
)


class AtividadeModel(Base):
    __tablename__ = "atividades"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    questoes = relationship("QuestaoModel", secondary=questoes_association, back_populates="atividades")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
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

    @staticmethod
    def update(session, client):
        with session.begin():
            session.merge(client)