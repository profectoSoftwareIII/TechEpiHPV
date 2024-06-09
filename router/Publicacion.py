import sys

sys.path.append("..")
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter
from utils.dbAlchemy import session
from models.models import (PublicacionModel, MedicoModel)
from schema.Publicacion import (PublicacionSchema, PublicacionBase)
from typing import List
import datetime

publicacion = APIRouter()


@publicacion.get("/publicacion_all/", response_model=List[PublicacionSchema])
async def get_publicaciones():
    publicaciones = session.query(PublicacionModel).all()
    return publicaciones
