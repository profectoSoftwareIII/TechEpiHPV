from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuración de conexión
username = os.getenv("root")
password = os.getenv("1234")
database = os.getenv("hpv_safe")
DB_URL = "mysql://root:1234@127.0.0.1/hpv_safe"

print(DB_URL)

# Intentar conectar a la base de datos
try:
    engine = create_engine("mysql+pymysql://root:1234@127.0.0.1/hpv_safe")
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error al conectar a la base de datos:")
    print(e)

session.close()
