import requests
import random
from datetime import datetime, timezone

TOKEN = "abc123"
SERVICE_NAME = "service_alpha"
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

headers = {"Authorization": f"Token {TOKEN}"}                 # Arma el header de autenticación con el token del servicio
logs = [generate_log() for _ in range(5)]                     # Genera una lista de 5 logs llamando a generate_log() 5 veces

response = requests.post(URL, json=logs, headers=headers)     # Envía los 5 logs de una sola vez al servidor con POST

print("Status:", response.status_code)                        # Muestra el código de respuesta del servidor: 201 si se guardaron, 401 si el token es inválido
print("Response:", response.json())                           # Muestra la respuesta completa del servidor en formato JSON
