from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:123456789@127.0.0.1/hpv_safe')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()