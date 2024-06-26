from fastapi import FastAPI
from router.Usuario import user
from router.Consulta import consulta
from router.Recordatorio import recordatorio
from router.Paciente import paciente
from router.Publicacion import publicacion
from router.Medico import medico
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
app.include_router(consulta, prefix="/consulta", tags=["Consultas"])
app.include_router(recordatorio, prefix="/recordatorio", tags=["Recordatorios"])
app.include_router(medico, prefix="/medico", tags=["Medicos"])
app.include_router(paciente, prefix="/paciente", tags=["Pacientes"])
app.include_router(publicacion, prefix="/publicacion", tags=["Publiacaciones"])


@app.get("/")
def hello_world():
    return {"message": "Servidor ejecutandose"}
