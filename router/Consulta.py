import sys

sys.path.append("..")
from fastapi import APIRouter, HTTPException
from utils.dbAlchemy import session
from models.models import ConsultaModel, PacienteModel, MedicoModel
from schema.Consulta import ConsultaSchema, ConsultaBase
from typing import List
import datetime

consulta = APIRouter()


@consulta.get("/getConsultas/", response_model=List[ConsultaSchema])
async def get_consultas():
    consultas = session.query(ConsultaModel).all()
    for consulta in consultas:
        print(consulta)
    return consultas


@consulta.post(path="/registrarConsulta/", response_model=ConsultaSchema)
async def registrar_consulta(consulta: ConsultaBase):
    db_consulta = ConsultaModel(**consulta.dict())
    fecha_actual = datetime.datetime.now()
    fecha_consulta = db_consulta.fecha.date()
    if fecha_actual.date() == fecha_consulta:
        if 1 < len(db_consulta.descripcion) <= 200:
            session.add(db_consulta)
            session.commit()
            session.refresh(db_consulta)
            print("REGISTRADO:", db_consulta)
            return db_consulta


@consulta.get(path="/consultaPaciente/")
async def historial_paciente(id: int):
    historiales = session.query(ConsultaModel, MedicoModel).join(MedicoModel, MedicoModel.id == ConsultaModel.medico_id).all()

    resultado_json = []
    for item in historiales:
        tabla_data = item[0].__dict__
        tabla_data2 = item[1].__dict__
        resultado_json.append({
            key: value for key, value in tabla_data.items() if not key.startswith('_')
        })
        resultado_json.append({
            key: value for key, value in tabla_data2.items() if not key.startswith('_')
        })
    return resultado_json


