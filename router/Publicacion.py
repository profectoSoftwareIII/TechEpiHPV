from datetime import datetime
import sys

sys.path.append("..")
from fastapi import APIRouter, HTTPException
from utils.dbAlchemy import session
from models.models import PublicacionModel, MedicoModel, UsuarioModel
from schema.Publicacion import PublicacionSchema, PublicacionBase

import requests

publicacion = APIRouter()


@publicacion.get("/publicacion_all/")
async def get_publicaciones():
    """ "
    _summary_: Get all publications
    _description_: Get all publications
    _responses_:
        200:
            description: Return a list of publications
    """
    publicaciones = session.query(PublicacionModel).all()
    return publicaciones


def existe_imagen(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


@publicacion.post("/publicaciones/")
async def crear_publicacion(publicacion: PublicacionSchema):
    session = session
    publicacion_db = (
        session.query(PublicacionModel)
        .filter(PublicacionModel.titulo == publicacion.titulo)
        .first()
    )
    if publicacion_db:
        raise HTTPException(status_code=400, detail="El título ya existe")
    if publicacion.imagen and not existe_imagen(publicacion.imagen):
        raise HTTPException(status_code=400, detail="La imagen no existe")
    nueva_publicacion = PublicacionModel(
        titulo=publicacion.titulo,
        contenido=publicacion.contenido,
        imagen=publicacion.imagen,
        fecha_publicacion=publicacion.fecha_publicacion or datetime.now(),
    )
    session.add(nueva_publicacion)
    session.commit()
    session.refresh(nueva_publicacion)
    return nueva_publicacion
