import sys

sys.path.append("..")
from fastapi import APIRouter
from utils.dbAlchemy import session
from models.models import PublicacionModel, MedicoModel, UsuarioModel
from schema.Publicacion import PublicacionSchema, PublicacionBase

publicacion = APIRouter()


@publicacion.get("/publicacion_all/")
async def get_publicaciones():
    publicaciones = session.query(PublicacionModel).all()
    return publicaciones


# @publicacion.post(path="/registrarPublicacion/")
# async def crear_publicacione(publicacion: PublicacionBase):
#     db_publicacion = PublicacionModel(**publicacion.dict())
#     medico = (
#         session.query(MedicoModel)
#         .filter(MedicoModel.id == db_publicacion.medico_id)
#         .first()
#     )
#     usuario = (
#         session.query(UsuarioModel).filter(UsuarioModel.id == medico.usuario_id).first()
#     )
#     fecha_actual = datetime.datetime.now()
#     fecha_publicacion = db_publicacion.fecha_publicacion.date()

#     if usuario and fecha_actual.date() == fecha_publicacion:
#         if 0 < len(db_publicacion.imagen) <= 100:
#             try:
#                 resultado_json = []
#                 consulta_dict = {
#                     "titulo": db_publicacion.titulo,
#                     "contenido": db_publicacion.contenido,
#                     "imagen": db_publicacion.imagen,
#                     "fecha_publicacion": fecha_publicacion,
#                     "medico": usuario.nombre,
#                 }
#                 resultado_json.append(consulta_dict)
#                 session.add(db_publicacion)
#                 session.commit()
#                 session.refresh(db_publicacion)

#                 return resultado_json
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 print("Error al registrar la consulta:", e)
