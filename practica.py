import requests
import random
from datetime import datetime, timezone

TOKEN = "token-secreto-123"
SERVICE_NAME = "servicio1"
URL = "http://localhost:5000/logs"

SEVERITIES = ["INFO", "DEBUG", "ERROR", "WARNING"]
MESSAGES = [
    "Todo bien.",
    "Algo falló.",
    "Conectando a base de datos.",
    "Timeout inesperado.",
    "Usuario no encontrado."
]

def generate_log():
    # Función que genera un log aleatorio con los 4 campos requeridos por el servidor
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),  # Fecha y hora exacta del evento en formato UTC
        "service":   SERVICE_NAME,                             # Nombre del servicio que genera el log
        "severity":  random.choice(SEVERITIES),               # Elige un nivel de severidad al azar de la lista
        "message":   random.choice(MESSAGES)                  # Elige un mensaje al azar de la lista
    }
 # Genera una lista de 5 logs llamando a generate_log() 5 veces

mi_log = {
    "timestap": datetime.now(timezone.utc).isoformat(),
    "service" : "sebasthian lopez",
    "severity": SEVERITIES[3],
    "message" : MESSAGES[3]
    
}
# response = requests.post(
#     URL,
#     headers= {"Authorization" : "abc"},
#     json= mi_log
# )
# print("Status:", response.status_code)                        # Muestra el código de respuesta del servidor: 201 si se guardaron, 401 si el token es inválido
# print("Response:", response.json())                           # Muestra la respuesta completa del servidor en formato JSON


# ===================== EJERCICIO =====================
# Enviar una lista de logs al servidor y contar cuántos fueron aceptados (status 201)

HEADERS = {"Authorization": TOKEN}

def send_multiple_logs(logs):
    for log in logs:
        response = requests.post(
            URL,
            headers= {"Autorizacion": f"token {TOKEN}"},
            json = log
        )
        if response.status_code == 201:
            return True
        else:
            return False
            
            

    # recorre cada log de la lista
        # hace un POST al servidor con el log actual y los headers
        # si el status code es 201, incrementa exitosos
    # retorna exitosos

def main():
    lista_logs = [
        generate_log() for _ in range(5)
    ]
    exitoso = send_multiple_logs(lista_logs)
    print(f" los logs exitosos fueron: {exitoso}")
    # genera una lista de 5 logs usando generate_log() con list comprehension
    # llama a send_multiple_logs con esa lista y guarda el resultado
    # imprime cuántos logs fueron exitosos del total enviado

main()


# ===================== EJERCICIO =====================
# Enviar una lista de logs al servidor y contar cuántos fueron aceptados (status 201)
def send_multiple_logs(logs):

    for log in logs:
        response = requests.post(
            URL,
            headers= {"Authorization" : f"token {TOKEN}" },
            json = log
        )
        if response.status_code == 201:
            exitosos += 1
    return exitosos
# recorre cada log de la lista
        # hace un POST al servidor con el log actual y los headers
        # si el status code es 201, incrementa exitosos
    # retorna exitosos
    
def main():
    lista = [
        generate_log() for _ in range(5)
    ]
    exitoso = send_multiple_logs(lista)
    print(f"La cantidad de tokens validos son: {exitoso}")
# genera una lista de 5 logs usando generate_log() con list comprehension
    # llama a send_multiple_logs con esa lista y guarda el resultado
    # imprime cuántos logs fueron exitosos del total enviado


main()