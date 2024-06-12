import sys

sys.path.append("..")
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter
from TechEpiHPV.utils.dbAlchemy import session
from TechEpiHPV.models.models import (
    ConsultaModel,
    PacienteModel,
    MedicoModel,
    TratamientoModel,
    UsuarioModel,
)
from TechEpiHPV.schema.Consulta import ConsultaSchema, ConsultaBase
from TechEpiHPV.schema.Tratamiento import TratamientoBase, TratamientoSchema
from typing import List
import datetime

consulta = APIRouter()


@consulta.get("/tratamientos_all/", response_model=List[TratamientoSchema])
async def get_tratamientos():
    tratamientos = session.query(TratamientoModel).all()
    return tratamientos


@consulta.get("/getConsultas/", response_model=List[ConsultaSchema])
async def get_consultas():
    consultas = session.query(ConsultaModel).all()
    return consultas


@consulta.post("/tratamiento", response_model=TratamientoBase)
async def create_tratamiento(tratamiento: TratamientoBase):
    db_tratamiento = TratamientoModel(**tratamiento.model_dump())
    session.add(db_tratamiento)
    session.commit()
    session.refresh(db_tratamiento)
    return db_tratamiento


@consulta.post(path="/registrarConsulta/", response_model=ConsultaSchema)
async def registrar_consulta(consulta: ConsultaBase):
    db_consulta = ConsultaModel(**consulta.dict())
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
    fecha_actual = datetime.datetime.now()
    fecha_consulta = db_consulta.fecha.date()

    if usuario and fecha_actual.date() == fecha_consulta:


        if 1 < len(db_consulta.descripcion) <= 200:
            try:
                session.add(db_consulta)
                session.commit()
                session.refresh(db_consulta)
                return db_consulta
            except SQLAlchemyError as e:
                session.rollback()
                print("Error al registrar la consulta:", e)


from sqlalchemy.exc import SQLAlchemyError


@consulta.get(path="/consultaPaciente/")
async def historial_paciente(id: int):
    try:
        consultas = (session.query(ConsultaModel).filter(ConsultaModel.paciente_id == id).all())
        paciente = (session.query(PacienteModel).filter(PacienteModel.id == consultas[0].paciente_id).first())
        medico = (session.query(MedicoModel).filter(MedicoModel.id == consultas[0].medico_id).first())
        usuarioMedico = (session.query(UsuarioModel).filter(UsuarioModel.id == medico.usuario_id).first())
        usuarioPaciente = (session.query(UsuarioModel).filter(UsuarioModel.id == paciente.usuario_id).first())

        resultado_json = []
        for item in consultas:
            consulta_dict = {
                "medico": usuarioMedico.nombre,
                "tarjetaProfesional": medico.tarjeta_profesional,
                "especialidad": medico.especialidad,
                "paciente": usuarioPaciente.nombre,
                "cedula": usuarioPaciente.cedula,
                "nombre_diagnostico": item.nombre_diagnostico,
                "descripcion": item.descripcion,
                "fecha": item.fecha,
            }

            resultado_json.append(consulta_dict)
        return resultado_json
    except SQLAlchemyError as e:
        return {"error": "Error al realizar la consulta a la base de datos"}


@consulta.get(path="/consultaPaciente/{id}")
async def historial_paciente(id: int):
    try:
        consultas = (
            session.query(ConsultaModel).filter(ConsultaModel.paciente_id == id).all()
        )
        if not consultas:
            return {
                "error": "No se encontraron consultas para el paciente con id "
                         + str(id)
            }

        paciente = (
            session.query(PacienteModel)
            .filter(PacienteModel.id == consultas[0].paciente_id)
            .first()
        )
        medico = (
            session.query(MedicoModel)
            .filter(MedicoModel.id == consultas[0].medico_id)
            .first()
        )
        usuarioMedico = (
            session.query(UsuarioModel)
            .filter(UsuarioModel.id == medico.usuario_id)
            .first()
        )
        usuarioPaciente = (
            session.query(UsuarioModel)
            .filter(UsuarioModel.id == paciente.usuario_id)
            .first()
        )

        resultado_json = []
        for item in consultas:
            consulta_dict = {
                "medico": usuarioMedico.nombre,
                "tarjetaProfesional": medico.tarjeta_profesional,
                "especialidad": medico.especialidad,
                "paciente": usuarioPaciente.nombre,
                "cedula": usuarioPaciente.cedula,
                "nombre_diagnostico": item.nombre_diagnostico,
                "descripcion": item.descripcion,
                "fecha": item.fecha,
            }

            resultado_json.append(consulta_dict)
        return resultado_json
    except SQLAlchemyError as e:
        print("Error al realizar la consulta a la base de datos:", e)
        return {"error": "Error al realizar la consulta a la base de datos"}
