from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

# Configuración de conexión
<<<<<<< HEAD
username = os.getenv("DB_USERNAME_L")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
print(username, password == "NH2YBNCg0VA1aY6I", database)
=======
username = os.getenv("root")
password = os.getenv("1234")
database = os.getenv("hpv_safe")
DB_URL = "mysql://root:1234@127.0.0.1/hpv_safe"
>>>>>>> origin/modulo_prevencion


# DB_URL = f"mysql+pymysql://TestABC:TestABC@127.0.0.1/MySql80"

# DB_URL = f"mysql+pymysql://{username}:{password}@localhost:3306/{database}"
# Intentar conectar a la base de datos
try:
<<<<<<< HEAD
    DB_URL = f"mysql+pymysql://soft_admin:{password}@127.0.0.1/hpv_safe"
    engine = create_engine(DB_URL)
    # engine = create_engine("mysql://root:123456789@127.0.0.1/hpv_safe")
=======
    engine = create_engine("mysql+pymysql://root:1234@127.0.0.1/hpv_safe")
>>>>>>> origin/modulo_prevencion
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error al conectar a la base de datos:")
    print(e)

session.close()
