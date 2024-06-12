from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

# Configuración de conexión
username = os.getenv("DB_USERNAME_L")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
try:
    DB_URL = f"mysql+pymysql://soft_admin:{password}@127.0.0.1/hpv_safe"
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error al conectar a la base de datos:")
    print(e)

session.close()
