# Conceptos técnicos aplicados

Glosario de los conceptos usados en este proyecto, explicados en el contexto de la implementación.

---

## API REST

**REST** (Representational State Transfer) es un estilo arquitectónico para diseñar APIs HTTP. Una API REST organiza los recursos en URLs y usa los **métodos HTTP** para indicar la operación:

| Método | Acción |
|--------|--------|
| `GET` | Leer/consultar datos |
| `POST` | Crear un nuevo recurso |
| `PUT` | Reemplazar un recurso existente |
| `DELETE` | Eliminar un recurso |

En este proyecto, `/logs` es el recurso central:
- `POST /logs` → crear nuevos logs
- `GET /logs` → consultar logs existentes

---

## Flask

**Flask** es un microframework HTTP para Python. Su diseño minimalista permite construir APIs sin componentes innecesarios.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/logs", methods=["POST"])
def receive_logs():
    data = request.get_json()
    return jsonify({"status": "ok"}), 201
```

**Conceptos de Flask usados:**
- `@app.route()` — decorador que asocia una URL y método HTTP a una función
- `request.headers` — acceso a los headers HTTP de la petición entrante
- `request.get_json()` — parsea el body JSON de la request
- `request.args` — accede a los query parameters de la URL (`?key=value`)
- `jsonify()` — serializa un dict Python a JSON y setea el Content-Type correcto

---

## SQLite

**SQLite** es una base de datos relacional embebida: no requiere servidor separado, guarda todo en un único archivo `.db`.

Python incluye el módulo `sqlite3` en su librería estándar.

```python
import sqlite3

conn = sqlite3.connect("logs.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("INSERT INTO logs (message) VALUES (?)", ("hola",))
conn.commit()
```

**Conceptos clave:**
- `connect()` — abre (o crea) el archivo de base de datos
- `cursor` — objeto para ejecutar queries
- `execute()` / `executemany()` — ejecuta SQL simple o en lote
- `conn.commit()` — confirma la transacción (sin esto los cambios no se persisten)
- `?` como placeholder — evita **SQL Injection** al separar la query de los datos

---

## Autenticación por Token

La autenticación por token es un mecanismo stateless: el cliente incluye un secreto en cada request. El servidor lo valida sin necesidad de sesiones ni cookies.

**Convención usada (Token Bearer):**
```
Authorization: Token abc123
```

```python
auth = request.headers.get("Authorization", "")
token = auth.replace("Token ", "")

if token not in VALID_TOKENS.values():
    return jsonify({"error": "Unauthorized"}), 401
```

Los tokens se cargan desde `tokens.json` en el arranque del servidor, permitiendo múltiples servicios con credenciales independientes.

---

## Códigos de estado HTTP

Los códigos de estado son parte del protocolo HTTP e indican el resultado de una request:

| Código | Nombre | Cuándo usarlo |
|--------|--------|---------------|
| `200 OK` | Éxito | GET exitoso |
| `201 Created` | Creado | POST que crea un recurso |
| `401 Unauthorized` | No autorizado | Token ausente o inválido |
| `404 Not Found` | No encontrado | Recurso no existe |
| `500 Internal Server Error` | Error del servidor | Error inesperado en el backend |

---

## Query Parameters

Los query parameters son pares `clave=valor` que se añaden a la URL después de `?`. Permiten filtrar o paginar resultados sin cambiar el endpoint.

```
GET /logs?severity=ERROR&timestamp_start=2024-01-01T00:00:00Z
```

```python
args = request.args
if args.get("severity"):
    query += " AND severity = ?"
    params.append(args["severity"])
```

El patrón `WHERE 1=1` permite construir queries dinámicas de forma limpia: cada filtro se agrega con `AND` sin necesidad de verificar si es el primero.

---

## Timestamps y UTC

Los logs usan **ISO 8601** con zona horaria **UTC** para garantizar consistencia entre servicios que pueden estar en distintas zonas horarias.

```python
from datetime import datetime, timezone

now = datetime.now(timezone.utc).isoformat()
# → "2024-01-15T10:30:01.123456+00:00"
```

El servidor registra **dos timestamps**:
- `timestamp` — cuándo ocurrió el evento (informado por el cliente)
- `received_at` — cuándo llegó al servidor (generado por el servidor)

Esta distinción permite detectar retrasos en la entrega de logs.

---

## Envío en lote (Batch)

El endpoint acepta tanto un log individual como una lista, normalizando internamente:

```python
logs = request.get_json()
if not isinstance(logs, list):
    logs = [logs]  # convierte objeto único a lista
```

El uso de `executemany()` es más eficiente que múltiples `execute()` individuales para insertar varios registros en una sola operación.
