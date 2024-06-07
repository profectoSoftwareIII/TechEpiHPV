from typing import Optional
from pydantic import BaseModel
from schema.Usuario import UsuarioBase


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


class PacienteCreate(UsuarioBase):
    tipo_vpv: Optional[str] = None
    medico_id: Optional[int]
