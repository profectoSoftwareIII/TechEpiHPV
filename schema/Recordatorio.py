from pydantic import BaseModel, Field
from datetime import datetime


class RecordatorioBase(BaseModel):
    medico_id: int
    paciente_id: int
    tipo_recordatorio: str
    descripcion: str
    fecha: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class RecordatorioSchema(RecordatorioBase):
    id: int

    class Config:
        orm_mode = True
