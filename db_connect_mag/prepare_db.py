# coding: utf-8
from dotenv import load_dotenv
load_dotenv('.env')
from db_connect_mag_201710 import get_db_connection
db = get_db_connection()
from models import Paper, Base, _name_for_collection_relationship
Base.prepare(db.engine, reflect=True, name_for_collection_relationship=_name_for_collection_relationship)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db.engine)
session = Session()
