from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from router.Usuario import user
from router.Consulta import consulta
from router.Recordatorio import recordatorio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user, prefix='/user')
app.include_router(consulta, prefix='/consulta')
app.include_router(recordatorio, prefix='/recordatorio')


@app.get("/")
def hello_world():
    print("HOLA")
    return {"message": "Servidor ejecutandose"}
