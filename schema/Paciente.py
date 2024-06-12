from typing import Optional
from pydantic import BaseModel
from TechEpiHPV.schema.Usuario import UsuarioBase


class PacienteBase(BaseModel):
    usuario_id: int
    tipo_hpv: str


class PacienteSchema(PacienteBase):
    id: int

    class Config:
        orm_mode = True


class PacienteSchemaNombre(PacienteBase):
    id: int

    class Config:
        orm_mode = True


class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    edad: int
    telefono: str
    email: str


class PacienteCreate(UsuarioBase):
    tipo_hpv: Optional[str] = None
    doctor_id: Optional[int] = None


class PacienteInBD(PacienteCreate):
    id: int


class Paciente(PacienteBase):
    id: int

    class Config:
        orm_mode = True
