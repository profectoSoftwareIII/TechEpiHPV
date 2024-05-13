from pydantic import BaseModel


class MedicoBase(BaseModel):
    id: int
    usuario_id = int
    tarjeta_profesional = str
    especialidad = str


class MedicoSchema(MedicoBase):
    id: int

    class Config:
        orm_mode = True