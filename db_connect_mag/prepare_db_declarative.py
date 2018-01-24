# coding: utf-8
from dotenv import load_dotenv
load_dotenv('.env')
from models_declarative import Paper, Base
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db.engine)
