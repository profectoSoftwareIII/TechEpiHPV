from pydantic import BaseModel


class TratamientoBase(BaseModel):
    nombre: str
    descripcion: str


class TratamientoSchema(TratamientoBase):
    id: int

    class Config:
        orm_mode = True