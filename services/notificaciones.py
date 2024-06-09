from models.models import RecordatorioModel
import requests


def enviarCorreo(datos: RecordatorioModel):
    print("enviando correo")
    response = requests.get(
        "http://127.0.0.1:5000/correo?destino={}&asunto={}&mensaje={}&hash=ABC123".format(
            datos.destino, datos.asunto, datos.mensaje
        )
    )
    print(response)


def enviarSMS(datos: RecordatorioModel):
    print("enviando sms")
    response = requests.get(
        "http://127.0.0.1:5000/sms?destino={}&mensaje={}&hash=ABC123".format(
            datos.destino, datos.mensaje
        )
    )
    print(response)
