import sys

sys.path.append("..")
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from fastapi import APIRouter
from typing import List
from TechEpiHPV.utils.dbAlchemy import session
from TechEpiHPV.models.models import (
    PacienteModel,
)
from TechEpiHPV.schema.Paciente import (
    PacienteCreate,
    PacienteInBD,
    PacienteSchema,
)

paciente = APIRouter()


@paciente.get("/pacientes_all/", response_model=List[PacienteSchema])
async def get_pacientes():
    pacientes = session.query(PacienteModel).all()
    return pacientes


@paciente.post("/registrar/", response_model=PacienteInBD)
def crear_paciente(paciente: PacienteCreate):
    try:
        db_paciente = PacienteModel(**paciente.model_dump())
        session.add(db_paciente)
        session.commit()
        session.refresh(db_paciente)
        return db_paciente
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"{e}")
