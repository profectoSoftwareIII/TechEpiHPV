from pydantic import BaseModel
from datetime import datetime


class PublicacionBase(BaseModel):
    medico_id: int
    titulo: str
    contenido: str
    imagen: str
    fecha_publicacion: datetime


class PublicacionSchema(PublicacionBase):
    id: int

    class Config:
        orm_mode = True
