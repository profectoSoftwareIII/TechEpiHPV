import sys
from fastapi import APIRouter, HTTPException
from TechEpiHPV.models.models import MedicoModel
from TechEpiHPV.schema.Paciente import Paciente, PacienteCreate, PacienteInBD, PacienteSchema
from TechEpiHPV.utils.dbAlchemy import session
from TechEpiHPV.schema.Medico import DoctorWithPacientes, MedicoSchema

sys.path.append("..")

medico = APIRouter()


@medico.get("/all_patiens_by_doctor/{medico_id}")
def obtener_pacientes_doctor(medico_id: int):
    query = session.query(MedicoModel).filter(MedicoModel.id == medico_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"medico": query, "pacientes": query.paciente}


@medico.get("/pacientes_by_doctor/{medico_id}", response_model=DoctorWithPacientes)
def obtener_pacientes_doctor(medico_id: int):
    query = session.query(MedicoModel).filter(MedicoModel.id == medico_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor_data = {
        "id": query.id,
        "nombre": query.usuario.nombre,
        "apellido": query.usuario.apellido,
        "cedula": query.usuario.cedula,
        "edad": query.usuario.edad,
        "telefono": query.usuario.telefono,
        "email": query.usuario.email,
        "especialidad": query.especialidad,
        "pacientes": [
            {
                "id": paciente.id,
                "nombre": paciente.nombre,
                "apellido": paciente.apellido,
                "cedula": paciente.cedula,
                "edad": paciente.edad,
                "telefono": paciente.telefono,
                "email": paciente.email,
                "tipo": paciente.tipo,
                "tipo_hpv": paciente.tipo_hpv,
                "doctor_id": paciente.doctor_id,
            }
            for paciente in query.paciente
        ],
    }

    return doctor_data
