import re
import sys

sys.path.append("..")
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from fastapi import APIRouter
from utils.dbAlchemy import session
from models.models import (
    PacienteModel,
    UsuarioModel,
)
from schema.Paciente import (
    PacienteCreate,
    PacienteInBD,
)

paciente = APIRouter()


@paciente.get("/pacientes_all/")
async def get_pacientes():
    pacientes = session.query(UsuarioModel).filter_by(tipo="paciente").all()
    return pacientes


@paciente.post("/registrar/", response_model=PacienteInBD)
def crear_paciente(paciente: PacienteCreate):
    """ "
    _summary_: Create a new patient
    description: Create a new patient
    _parameters_:
        - paciente: PacienteCreate
    _responses_:
        200:
            description: Return the patient created
        400:
            description: The patient already exists
        400:
            description: The patient must be at least 18 years old
        400:
            description: The email is not valid

    """
    # Verificar la unicidad de la cédula
    db_paciente = (
        session.query(PacienteModel)
        .filter(PacienteModel.cedula == paciente.cedula)
        .first()
    )
    if db_paciente:
        raise HTTPException(status_code=400, detail="La cédula ya está en uso")

    # Verificar la edad mínima
    if paciente.edad < 18:
        raise HTTPException(
            status_code=400, detail="El paciente debe tener al menos 18 años"
        )

    # Verificar el formato del correo electrónico
    if not re.match(r"[^@]+@[^@]+\.[^@]+", paciente.email):
        raise HTTPException(
            status_code=400, detail="El correo electrónico no es válido"
        )
    try:
        db_paciente = PacienteModel(**paciente.dict())
        session.add(db_paciente)
        session.commit()
        session.refresh(db_paciente)
        return db_paciente
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"{e}")
