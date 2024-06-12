import sys

sys.path.append("..")
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter
from TechEpiHPV.utils.dbAlchemy import session
from TechEpiHPV.models.models import (PublicacionModel, MedicoModel, UsuarioModel)
from TechEpiHPV.schema.Publicacion import (PublicacionSchema, PublicacionBase)
from typing import List
from fastapi import APIRouter, HTTPException
import datetime

publicacion = APIRouter()


@publicacion.get("/publicacion_all/", response_model=List[PublicacionSchema])
async def get_publicaciones():
    publicaciones = session.query(PublicacionModel).all()
    return publicaciones


@publicacion.post(path="/registrarPublicacion/")
async  def crear_publicacione(publicacion: PublicacionBase):
    db_publicacion = PublicacionModel(**publicacion.dict())
    fecha_actual = datetime.datetime.now()
    fecha_publicacion = db_publicacion.fecha_publicacion.date()

    if fecha_actual.date() == fecha_publicacion:
        if 0 < len(db_publicacion.imagen) <= 100:
            try:
                resultado_json = []
                consulta_dict = {
                    "titulo": db_publicacion.titulo,
                    "contenido": db_publicacion.contenido,
                    "imagen": db_publicacion.imagen,
                    "fecha_publicacion": fecha_publicacion
                }
                resultado_json.append(consulta_dict)
                session.add(db_publicacion)
                session.commit()
                session.refresh(db_publicacion)
                print(consulta_dict)
                return consulta_dict
            except SQLAlchemyError as e:
                session.rollback()
                print("Error al registrar la consulta:", e)
        else:
            raise HTTPException(status_code=404, detail="Numero de caracteres excedio el limite")
    else:
        raise HTTPException(status_code=404, detail="Fecha incorrecta")
