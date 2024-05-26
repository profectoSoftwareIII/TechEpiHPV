from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuración de conexión
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
DB_URL = f"mysql+pymysql://{username}:{password}@127.0.0.1/{database}"


# Intentar conectar a la base de datos
try:
    engine = create_engine(DB_URL)
    # engine = create_engine("mysql://root:123456789@127.0.0.1/hpv_safe")
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error al conectar a la base de datos:")
    print(e)

session.close()
