import sys

sys.path.append("..")
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter
from utils.dbAlchemy import session
from models.models import (PublicacionModel, MedicoModel, UsuarioModel)
from schema.Publicacion import (PublicacionSchema, PublicacionBase)
from typing import List
import datetime

publicacion = APIRouter()


@publicacion.get("/publicacion_all/", response_model=List[PublicacionSchema])
async def get_publicaciones():
    publicaciones = session.query(PublicacionModel).all()
    return publicaciones


@publicacion.post("/creaPublicacion/", response_model=PublicacionSchema)
async def crear_publicacion(publicacion: PublicacionBase):
    db_publicacion = PublicacionModel(**publicacion.dict())
    medico = session.query(MedicoModel).filter(MedicoModel.id == db_publicacion.medico_id).first()
    usuario = session.query(UsuarioModel).filter(UsuarioModel.id == medico.usuario_id).first()

    if medico and db_publicacion.imagen != "" and 0 < len(db_publicacion.contenido) < 100:
        try:

            resultado_json = []
            consulta_dict = {
                "contenido": db_publicacion.contenido,
                "titulo": db_publicacion.titulo,
                "imagen": db_publicacion.imagen,
                "fecha_publicacion": db_publicacion.fecha_publicacion,
                "medico": usuario.nombre
            }

            resultado_json.append(consulta_dict)

            session.add(db_publicacion)
            session.commit()
            session.refresh(db_publicacion)

            return db_publicacion
        except SQLAlchemyError as e:
            session.rollback()
            print("Error al registrar la consulta:", e)
