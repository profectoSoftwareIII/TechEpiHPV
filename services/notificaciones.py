import requests

from models.models import notificacionesModel


async def enviarCorreo(destino, asunto, mensaje):
    response = requests.get(
        "http://127.0.0.1:5000/correo?destino={}&asunto={}&mensaje={}&hash=ABC123".format(
            destino, asunto, mensaje
        )
    )
    print(response)


async def enviarSMS(destino, mensaje):
    response = requests.get(
        "http://127.0.0.1:5000/sms?destino={}&mensaje={}&hash=ABC123".format(
            destino, mensaje
        )
    )
    print(response)
