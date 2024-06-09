from pydantic import BaseModel


class PublicacionBase(BaseModel):
    medico_id: int
    titulo: str
    contenido: str
    imagen: str
    nombre: str


class PublicacionSchema(PublicacionBase):
    id: int

    class Config:
        orm_mode = True
