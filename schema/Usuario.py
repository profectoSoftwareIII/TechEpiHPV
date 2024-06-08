from pydantic import BaseModel


class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    edad: int
    telefono: str
    email: str


class UsuarioSchema(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
