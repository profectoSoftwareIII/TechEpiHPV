import sys

sys.path.append("..")
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter
from utils.dbAlchemy import session
from models.models import (
    ConsultaModel,
    PacienteModel,
    MedicoModel,
    TratamientoModel,
    UsuarioModel,
)
from schema.Paciente import (
    Paciente,
    PacienteCreate,
    PacienteInBD,
    PacienteSchema,
    PacienteBase,
    PacienteSchemaNombre,
)


from typing import List
import datetime

paciente = APIRouter()


@paciente.get("/pacientes_all/", response_model=List[PacienteSchema])
async def get_pacientes():
    pacientes = session.query(PacienteModel).all()
    return pacientes


from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorModel(BaseModel):
    error: str


@paciente.post("/registrar/", response_model=PacienteInBD)
def crear_paciente(paciente: PacienteCreate):
    try:
        db_paciente = PacienteModel(**paciente.dict())
        session.add(db_paciente)
        session.commit()
        session.refresh(db_paciente)
        return db_paciente
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"{e}")
