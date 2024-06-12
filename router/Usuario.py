import sys

sys.path.append("..")
from fastapi import APIRouter
from TechEpiHPV.schema.Usuario import UsuarioSchema
from TechEpiHPV.utils.dbAlchemy import session
from TechEpiHPV.models.models import UsuarioModel
from TechEpiHPV.schema.Usuario import UsuarioSchema
from typing import List

user = APIRouter()


@user.get("/all/", response_model=List[UsuarioSchema])
async def get_users():
    usuarios = session.query(UsuarioModel).all()
    for user in usuarios:
        print(user.nombre)
    return usuarios
