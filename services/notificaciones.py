from models.models import notificacionesModel
import requests


def enviarCorreo(datos: notificacionesModel):
    print('Enviando correo...', datos.asunto, datos.destino, datos.mensaje)
    response = requests.get('http://127.0.0.1:8000/correo?destino={}&asunto={}&mensaje={}&hash=ABC123'
                            .format(datos.destino, datos.asunto, datos.mensaje))
    print(response)


def enviarSMS(datos: notificacionesModel):
    print('Enviando correo...', datos.asunto, datos.destino, datos.mensaje)
    response = requests.get('http://127.0.0.1:8000/sms?destino={}&asunto={}&mensaje={}&hash=ABC123'
                            .format(datos.destino, datos.asunto, datos.mensaje))
    print(response)