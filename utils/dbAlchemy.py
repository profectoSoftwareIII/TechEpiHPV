from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('DIRE-DATABASE')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()