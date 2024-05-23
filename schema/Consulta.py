from pydantic import BaseModel
from datetime import datetime


class ConsultaBase(BaseModel):
    paciente_id: int
    medico_id: int
    tratamiento_id: int
    nombre_diagnostico: str
    descripcion: str
    fecha: datetime


class ConsultaSchema(ConsultaBase):
    id: int

    class Config:
        orm_mode = True


class TratamientoBase(BaseModel):
    nombre: str
    descripcion: str


class ConsultaTratamientoSchema(TratamientoBase):
    id: int

    class Config:
        orm_mode = True
