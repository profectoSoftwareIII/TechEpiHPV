from pydantic import BaseModel
from datetime import datetime


class HistorialDiagnosticoBase(BaseModel):
    id: int
    paciente_id = int
    medico_id = int
    fecha = datetime


class HistorialDiagnosticoSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True
