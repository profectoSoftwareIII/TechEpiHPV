from pydantic import BaseModel


class PoblacionGeneralBase(BaseModel):
    usuario_id: int
    ocupacion: str
    ubicacion: str


class PoblacionGeneralSchema(PoblacionGeneralBase):
    id: int

    class Config:
        orm_mode = True