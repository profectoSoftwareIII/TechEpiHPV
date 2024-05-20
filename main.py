from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from router.Usuario import user
from router.Consulta import consulta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user, prefix='/user')
app.include_router(consulta, prefix='/consulta')


@app.get("/")
def hello_world():
    print("HOLA")
    return {"message": "Servidor ejecutandose"}
