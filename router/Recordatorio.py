import sys

sys.path.append("..")
from fastapi import APIRouter, HTTPException
from utils.dbAlchemy import session
from models.models import RecordatorioModel, PacienteModel, UsuarioModel, notificacionesModel
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
    item = (session.query(RecordatorioModel, PacienteModel, UsuarioModel).
            join(RecordatorioModel, RecordatorioModel.paciente_id == PacienteModel.id).first())

    if item[0].tipo_recordatorio == "email":
        notificacionesModel.destino = item[2].email
        notificacionesModel.asunto = 'RECORDATORIO DINAMICO'
        notificacionesModel.mensaje = item[0].descripcion
        notificacion = notificaciones.enviarCorreo(notificacionesModel)

    elif item[0].tipo_recordatorio == "telefono":
        notificacionesModel.destino = item[2].telefono
        notificacionesModel.asunto = 'RECORDATORIO DINAMICO'
        notificacionesModel.mensaje  = item[0].descripcion
        notificacion = notificaciones.enviarSMS(notificacionesModel)

    return db_consulta
