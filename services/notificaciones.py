from models.models import notificacionesModel
import requests


def enviarCorreo(datos: notificacionesModel):
    print("enviando correo")
    response = requests.get('http://127.0.0.1:5000/correo?destino={}&asunto={}&mensaje={}&hash=ABC123'
                            .format(datos.destino, datos.asunto, datos.mensaje))
    print(response)


def enviarSMS(datos: notificacionesModel):
    print("enviando sms")
    response = requests.get('http://127.0.0.1:5000/sms?destino={}&mensaje={}&hash=ABC123'
                            .format(datos.destino, datos.mensaje))
    print(response)
