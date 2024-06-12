import sys

sys.path.append("..")
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, HTTPException
from utils.dbAlchemy import session
from sqlalchemy.exc import SQLAlchemyError
from models.models import (
    ConsultaModel,
    PacienteModel,
    MedicoModel,
    TratamientoModel,
    UsuarioModel,
)
from schema.Consulta import ConsultaSchema, ConsultaBase
from schema.Tratamiento import TratamientoBase, TratamientoSchema
from typing import List
import datetime
from sqlalchemy.orm import joinedload

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
    fecha_actual = datetime.datetime.now()
    fecha_consulta = db_consulta.fecha.date()
    if fecha_consulta != fecha_actual.date():
        raise HTTPException(
            status_code=400, detail="La fecha de la consulta debe ser el día actual."
        )
    if not (1 < len(db_consulta.descripcion) <= 200):
        raise HTTPException(
            status_code=400,
            detail="La descripción debe tener entre 2 y 200 caracteres.",
        )
    try:
        session.add(db_consulta)
        session.commit()
        session.refresh(db_consulta)
        return db_consulta
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=500, detail="Error al registrar la consulta: {}".format(e)
        )


@consulta.get("/consultasPaciente/{paciente_id}")
def consultar_consultas_paciente(paciente_id: int):
    # Inicia una sesión de SQLAlchemy
    db = session

    # Busca al paciente por su ID con sus consultas y los datos del médico
    paciente = (
        db.query(PacienteModel)
        .filter(PacienteModel.id == paciente_id)
        .options(joinedload(PacienteModel.consulta).joinedload(ConsultaModel.medico))
        .first()
    )

    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Serializa los datos de las consultas en formato JSON
    paciente_json = {
        "id": paciente.id,
        "nombre": paciente.nombre,
        "apellido": paciente.apellido,
        "cedula": paciente.cedula,
        "edad": paciente.edad,
        "telefono": paciente.telefono,
        "email": paciente.email,
        "consultas": [],
    }

    # Agrega las consultas del paciente a la lista de consultas en el JSON del paciente
    for consulta in paciente.consulta:
        consulta_data = {
            "id": consulta.id,
            "nombre_diagnostico": consulta.nombre_diagnostico,
            "tratamiento": consulta.tratamiento.nombre,
            "descripcion": consulta.descripcion,
            "fecha": consulta.fecha.strftime("%Y-%m-%d %I:%M %p"),
            "medico": {
                "id": consulta.medico.id,
                "tarjeta_profesional": consulta.medico.tarjeta_profesional,
                "especialidad": consulta.medico.especialidad,
                "nombre": consulta.medico.usuario.nombre,
                "apellido": consulta.medico.usuario.apellido,
                "cedula": consulta.medico.usuario.cedula,
                "edad": consulta.medico.usuario.edad,
                "telefono": consulta.medico.usuario.telefono,
                "email": consulta.medico.usuario.email,
            },
        }
        paciente_json["consultas"].append(consulta_data)

    return paciente_json
