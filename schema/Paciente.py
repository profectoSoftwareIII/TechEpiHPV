from pydantic import BaseModel


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


