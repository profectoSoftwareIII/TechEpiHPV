from pydantic import BaseModel


class PoblacionGeneralBase(BaseModel):
    id: int
    usuario_id: int


class PoblacionGeneralSchema(PoblacionGeneralBase):
    id: int

    class Config:
        orm_mode = True