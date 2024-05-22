import sys

sys.path.append("..")
from fastapi import APIRouter, HTTPException
from utils.dbAlchemy import session
from models.models import RecordatorioModel, PacienteModel, UsuarioModel, notificacionesModel, ConsultaModel
from schema.Recordatorio import RecordatorioSchema, RecordatorioBase
from services import notificaciones
from typing import List
import datetime

recordatorio = APIRouter()


@recordatorio.get("/getRecordatorios/", response_model=List[RecordatorioSchema])
async def get_consultas():
    recordatorios = session.query(RecordatorioModel).all()
    for recordatorio in recordatorios:
        print(recordatorio)
    return recordatorios


@recordatorio.post(path="/registrarRecordatorio/", response_model=RecordatorioSchema)
async def resgistrar_recordatorio(recordatorio: RecordatorioBase):
    db_consulta = RecordatorioModel(**recordatorio.dict())
    session.add(db_consulta)
    session.commit()
    session.refresh(db_consulta)
    paciente = session.query(PacienteModel).filter(PacienteModel.id == db_consulta.paciente_id).first()
    usuario = session.query(UsuarioModel).filter(UsuarioModel.id == paciente.usuario_id).first()
    consulta = session.query(ConsultaModel).filter(ConsultaModel.paciente_id == paciente.id).first()

    if db_consulta.tipo_recordatorio == "email":
        notificacionesModel.destino = usuario.email
        notificacionesModel.asunto = 'RECORDATORIO DINAMICO'
        notificacionesModel.mensaje = consulta.descripcion

    elif db_consulta.tipo_recordatorio == "telefono":
        notificacionesModel.destino = usuario.telefono
        notificacionesModel.asunto = 'RECORDATORIO DINAMICO'
        notificacionesModel.mensaje  = consulta.descripcion


    return db_consulta
