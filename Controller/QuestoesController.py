from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Model.QuestoesModel import QuestaoModel
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv('DATABASE_URL')

class QuestoesController:
    def __init__(self):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)