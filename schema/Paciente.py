from pydantic import BaseModel


class PacienteBase(BaseModel):
    usuario_id: str
    tipo_hpv: str


class PacienteSchema(PacienteBase):
    id: int

    class Config:
        orm_mode = True