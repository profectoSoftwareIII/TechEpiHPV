from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from router.Usuario import user
from router.Consulta import consulta
from router.Recordatorio import recordatorio
from router.Paciente import paciente
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(user, prefix="/user")
app.include_router(consulta, prefix="/consulta")
app.include_router(recordatorio, prefix="/recordatorio")
app.include_router(paciente, prefix="/paciente")


@app.get("/")
def hello_world():
    return {"message": "Servidor ejecutandose"}
