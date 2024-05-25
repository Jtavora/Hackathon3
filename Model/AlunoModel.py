from sqlalchemy.orm import relationship
from sqlalchemy import *
import uuid
from datetime import datetime
from Model.Base import Base

def generate_uuid():
    return str(uuid.uuid4())

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
    def get_all(session):
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
