import sys

sys.path.append("..")
from fastapi import APIRouter
from TechEpiHPV.utils.dbAlchemy import session
from TechEpiHPV.models.models import (
    RecordatorioModel,
    PacienteModel,
    RecordatorioModel,
    UsuarioModel,
    ConsultaModel,
)
from TechEpiHPV.schema.Recordatorio import RecordatorioSchema, RecordatorioBase
from TechEpiHPV.services import notificaciones
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


@recordatorio.post(path="/registrarRecordatorio/", response_model=RecordatorioSchema)
async def resgistrar_recordatorio(recordatorio: RecordatorioBase):
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
    try:
        if db_consulta.tipo_recordatorio == "email":
            RecordatorioModel.destino = usuario.email
            RecordatorioModel.asunto = "RECORDATORIO DINAMICO"
            RecordatorioModel.mensaje = consulta.descripcion
            notificaciones.enviarCorreo(RecordatorioModel)

        elif db_consulta.tipo_recordatorio == "telefono":
            RecordatorioModel.destino = usuario.telefono
            RecordatorioModel.mensaje = consulta.descripcion
            notificaciones.enviarSMS(RecordatorioModel)
        return db_consulta
    except SQLAlchemyError as e:
        session.rollback()
