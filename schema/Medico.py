from typing import List, Optional
from pydantic import BaseModel


class MedicoBase(BaseModel):
    usuario_id: int
    tarjeta_profesional: str
    especialidad: str


class MedicoSchema(MedicoBase):
    id: int

    class Config:
        orm_mode = True


class PacienteBase(BaseModel):
    id: int
    nombre: str
    apellido: str
    cedula: str
    edad: str
    genero: str
    telefono: str
    email: str
    tipo: str
    tipo_hpv: Optional[str]
    doctor_id: Optional[int]

    class Config:
        orm_mode = True


class DoctorWithPacientes(BaseModel):
    id: int
    nombre: str
    apellido: str
    cedula: str
    edad: str
    telefono: str
    email: str
    especialidad: str
    pacientes: List[PacienteBase]

    class Config:
        orm_mode = True
