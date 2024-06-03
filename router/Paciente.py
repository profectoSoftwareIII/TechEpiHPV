import sys

sys.path.append("..")
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
from schema.Paciente import PacienteSchema, PacienteBase, PacienteSchemaNombre


from typing import List
import datetime

paciente = APIRouter()


@paciente.get("/pacientes_all/", response_model=List[PacienteSchema])
async def get_pacientes():
    pacientes = session.query(PacienteModel).all()
    return pacientes


# generate endpoint create paciente
@paciente.post(path="/registrarPaciente/", response_model=PacienteSchema)
async def resgistrar_paciente(paciente: PacienteBase):
    try:
        db_paciente = PacienteModel(**paciente.model_dump())
        session.add(db_paciente)
        session.commit()
        session.refresh(db_paciente)
        return db_paciente
    except SQLAlchemyError as e:
        session.rollback()
        return {"error": "Error al realizar la consulta a la base de datos"}
