import sys

sys.path.append("..")
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter
from utils.dbAlchemy import session
from models.models import (ConsultaModel, PacienteModel, MedicoModel, TratamientoModel, UsuarioModel)
from schema.Paciente import (PacienteSchema, PacienteBase,PacienteSchemaNombre)


from typing import List
import datetime

paciente = APIRouter()

@paciente.get("/pacientes_all/", response_model=List[PacienteSchema])
async def get_pacientes():
    
    
    pacientes = session.query(PacienteModel).all()


    return pacientes