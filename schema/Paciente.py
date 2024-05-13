from pydantic import BaseModel


class PacienteBase(BaseModel):
    id: int
    usuario_id = str


class PacienteSchema(PacienteBase):
    id: int

    class Config:
        orm_mode = True