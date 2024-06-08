from fastapi import APIRouter, HTTPException
from models.models import MedicoModel
from utils.dbAlchemy import session

doctor = APIRouter()


@doctor.get("/pacientes_by_doctor/{medico_id}")
def obtener_pacientes_doctor(medico_id: int):
    query = session.query(MedicoModel).filter(MedicoModel.id == medico_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor.pacientes
