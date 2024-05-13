from pydantic import BaseModel
from datetime import datetime


class RecordatorioBase(BaseModel):
    id: int
    medico_id = int
    paciente_id = int
    tipo_recordatorio = str
    descripcion = str
    fecha = datetime


class RecordatorioSchema(RecordatorioBase):
    id: int

    class Config:
        orm_mode = True
