import sys

sys.path.append("..")
from fastapi import APIRouter, HTTPException
from utils.dbAlchemy import session
from models.models import ConsultaModel, PacienteModel, MedicoModel, UsuarioModel
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
    consultas = session.query(ConsultaModel).filter(ConsultaModel.paciente_id == id).all()
    paciente = session.query(PacienteModel).filter(PacienteModel.id == consultas[0].paciente_id).first()
    medico = session.query(MedicoModel).filter(MedicoModel.id == consultas[0].medico_id).first()
    usuarioMedico = session.query(UsuarioModel).filter(UsuarioModel.id == medico.usuario_id).first()
    usuarioPaciente = session.query(UsuarioModel).filter(UsuarioModel.id == paciente.usuario_id).first()

    resultado_json = []
    for item in consultas:
        consulta_dict = {
            'medico': usuarioMedico.nombre,
            'tarjetaProfesional': medico.tarjeta_profesional,
            'especialidad': medico.especialidad,
            'paciente': usuarioPaciente.nombre,
            'cedula': usuarioPaciente.cedula,
            'nombre_diagnostico': item.nombre_diagnostico,
            'descripcion': item.descripcion,
            'fecha': item.fecha
        }

        resultado_json.append(consulta_dict)
    return resultado_json
