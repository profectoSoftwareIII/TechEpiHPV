import sys

sys.path.append("..")
from fastapi import APIRouter
from utils.dbAlchemy import session
from models.models import (
    RecordatorioModel,
    PacienteModel,
    UsuarioModel,
    notificacionesModel,
    ConsultaModel,
)
from schema.Recordatorio import RecordatorioSchema, RecordatorioBase
from services import notificaciones
from typing import List
from sqlalchemy.exc import SQLAlchemyError

import datetime

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


@recordatorio.post(path="/registrarRecordatorio/", response_model=RecordatorioSchema)
async def resgistrar_recordatorio(recordatorio: RecordatorioBase):
    try:
        db_consulta = RecordatorioModel(**recordatorio.dict())
        session.add(db_consulta)
        session.commit()
        session.refresh(db_consulta)
        paciente = (
            session.query(PacienteModel)
            .filter(PacienteModel.id == db_consulta.paciente_id)
            .first()
        )
        usuario = (
            session.query(UsuarioModel)
            .filter(UsuarioModel.id == paciente.usuario_id)
            .first()
        )
        consulta = (
            session.query(ConsultaModel)
            .filter(ConsultaModel.paciente_id == paciente.id)
            .first()
        )

        if db_consulta.tipo_recordatorio == "email":
            notificacionesModel.destino = usuario.email
            notificacionesModel.asunto = "RECORDATORIO DINAMICO"
            notificacionesModel.mensaje = consulta.descripcion

        elif db_consulta.tipo_recordatorio == "telefono":
            notificacionesModel.destino = usuario.telefono
            notificacionesModel.asunto = "RECORDATORIO DINAMICO"
            notificacionesModel.mensaje = consulta.descripcion

        return db_consulta
    except SQLAlchemyError as e:
        session.rollback()
        print("Error al registrar el recordatorio:", e)
        return {"error": "Error al registrar el recordatorio"}
