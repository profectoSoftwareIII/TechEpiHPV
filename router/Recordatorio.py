from datetime import date
import sys

sys.path.append("..")
from fastapi import APIRouter, HTTPException
from utils.dbAlchemy import session
from models.models import (
    RecordatorioModel,
    PacienteModel,
    RecordatorioModel,
)
from schema.Recordatorio import RecordatorioSchema, RecordatorioBase
from services import notificaciones
from typing import List
from sqlalchemy.exc import SQLAlchemyError


recordatorio = APIRouter()


@recordatorio.get("/getRecordatorios/", response_model=List[RecordatorioSchema])
async def get_consultas():
    try:
        recordatorios = session.query(RecordatorioModel).all()
        for recordatorio in recordatorios:
            print(recordatorio)
        return recordatorios
    except SQLAlchemyError as e:
        print("Error al realizar la consulta a la base de datos:", e)
        return {"error": "Error al realizar la consulta a la base de datos"}


@recordatorio.post("/registrarRecordatorio/")
async def create_recordatorio(recordatorio: RecordatorioBase):
    """_summary_
    Create a new reminder for a patient with a specific type of reminder
    email and phone
    """
    try:
        db = session
        paciente = (
            db.query(PacienteModel)
            .filter(PacienteModel.id == recordatorio.paciente_id)
            .first()
        )
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")

        # Verificar si la fecha del recordatorio es mayor o igual a la fecha actual
        if recordatorio.fecha.date() < date.today():
            raise HTTPException(
                status_code=400,
                detail="La fecha del recordatorio debe ser igual o mayor a la fecha actual",
            )

        db_recordatorio = RecordatorioModel(**recordatorio.model_dump())
        db.add(db_recordatorio)
        db.commit()
        db.refresh(db_recordatorio)
        if recordatorio.tipo_recordatorio == "email":
            asunto = "Recordatorio Importante: Prevención del Virus del Papiloma Humano (VPH)"
            await notificaciones.enviarCorreo(
                paciente.email, asunto, recordatorio.descripcion
            )
        elif recordatorio.tipo_recordatorio == "telefono":
            print("ES TELEFONO")
            await notificaciones.enviarSMS(paciente.telefono, recordatorio.descripcion)
        else:
            raise HTTPException(status_code=400, detail="Tipo de recordatorio inválido")

        return db_recordatorio
    except Exception as e:
        # Aquí puedes manejar la excepción como prefieras
        print(e)
        raise
