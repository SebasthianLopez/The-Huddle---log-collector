# Importaciones necesarias para la app
from flask import Flask, request, jsonify, redirect  # Flask para el servidor HTTP, request para leer datos entrantes, jsonify para responder en JSON
import sqlite3                             # Driver para la base de datos SQLite
from datetime import datetime, timezone   # Para generar timestamps con zona horaria UTC
import json                               # Para leer el archivo tokens.json

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Carga de tokens válidos desde archivo externo
with open("tokens.json") as f:
    VALID_TOKENS = json.load(f)

def is_token_valid(token):
    """Verifica si el token recibido está en la lista de tokens válidos"""
    # Se compara contra los valores (tokens) del diccionario
    return token in VALID_TOKENS.values()


# Conexión a la base de datos SQLite 
# check_same_thread=False permite usar la misma conexión desde distintos contextos de Flask
conn = sqlite3.connect("logs.db", check_same_thread=False)
cursor = conn.cursor()

# Creación de la tabla de logs si no existe todavía
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    service TEXT,
    severity TEXT,
    message TEXT,
    received_at TEXT
)
""")
conn.commit()  # Confirma la creación de la tabla en la DB

# Redirect de / a /logs para que la URL raíz funcione
# decorador
@app.route("/")
def index():
    return redirect("/logs")

# Endpoint /logs: maneja POST (recibir logs) y GET (consultar logs)
# es una funcion que modifica otra funcion. decorador
@app.route("/logs", methods=["GET", "POST"])
def logs():
    if request.method == "POST":
        return receive_logs()
    return get_logs()

def receive_logs():
    # Extrae el token del header Authorization (formato: "Token <valor>")
    # request.headers: Lee los datos ocultos
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Token ", "")

    # Rechaza la petición si el token no es válido
    if not is_token_valid(token):
        return jsonify({"error": "Quién sos, bro?"}), 401

    # Lee el cuerpo JSON; acepta tanto un objeto único como una lista de logs
    logs = request.get_json()
    if not isinstance(logs, list): # verifica si algo es de un tipo especifico.
        logs = [logs]  

    # Genera el timestamp de recepción en el servidor 
    now = datetime.now(timezone.utc).isoformat() # convierte una fecha a texto

    
    cursor.executemany("""
        INSERT INTO logs (timestamp, service, severity, message, received_at)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (log.get("timestamp"), log.get("service"),
        log.get("severity"), log.get("message"), now)
        for log in logs
    ])
    conn.commit()  

    return jsonify({"status": "Logs recibidos"}), 201

def get_logs():
    args = request.args  # Parámetros de la URL (?severity=ERROR&...)

    # Base de la query; WHERE 1=1 permite agregar AND dinámicamente sin condicionales extra
    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    # Filtro por rango de timestamp del cliente (hora del evento)
    if args.get("timestamp_start"):
        query += " AND timestamp >= ?"
        params.append(args["timestamp_start"])
    if args.get("timestamp_end"):
        query += " AND timestamp <= ?"
        params.append(args["timestamp_end"])

    # Filtro por nivel de severidad (ERROR, INFO, WARNING, etc.)
    if args.get("severity"):
        query += " AND severity = ?"
        params.append(args["severity"])

    # Filtro por rango de received_at (hora en que el servidor recibió el log)
    if args.get("received_at_start"):
        query += " AND received_at >= ?"
        params.append(args["received_at_start"])
    if args.get("received_at_end"):
        query += " AND received_at <= ?"
        params.append(args["received_at_end"])

    # Ejecuta la query con los parámetros seguros (evita SQL injection)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Convierte las filas en lista de dicts para serializar como JSON
    logs = [{
        "id": r[0], "timestamp": r[1], "service": r[2],
        "severity": r[3], "message": r[4], "received_at": r[5]
    } for r in rows]

    return jsonify(logs), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
