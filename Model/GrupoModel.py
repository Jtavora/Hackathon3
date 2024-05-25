from sqlalchemy.orm import relationship
from sqlalchemy import *
import uuid
from datetime import datetime
from Model.AlunoModel import generate_uuid
from Model.Base import Base

grupo_aluno_association = Table(
    'grupo_aluno', Base.metadata,
    Column('grupo_id', String(36), ForeignKey('grupos.id')),
    Column('aluno_id', String(36), ForeignKey('alunos.id')),
    UniqueConstraint('grupo_id', 'aluno_id', name='uix_grupo_aluno')
)

class GrupoAtividadeModel(Base):
    _tablename__="grupo_atividade"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    atividade_id = Column(String(36), ForeignKey('atividades.id'))
    sequencia_pontuacao = Column(Integer, default=0)
    pontuacao = Column(Integer, default=0)

    