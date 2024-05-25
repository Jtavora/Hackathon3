from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model.AtividadeModel import AtividadeModel
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv('DATABASE_URL')

class AtividadeController:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)