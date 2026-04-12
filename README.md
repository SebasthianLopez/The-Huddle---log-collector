# Log Collector API

API REST centralizada para recolección y consulta de logs de servicios, construida con Python y Flask.

## Descripción

Este proyecto implementa un servidor de logs que permite a múltiples servicios enviar sus registros de eventos a un punto centralizado. Los logs se persisten en SQLite y pueden consultarse con filtros flexibles.

## Stack

- **Python 3** — lenguaje base
- **Flask** — framework HTTP para la API REST
- **SQLite** — base de datos embebida para persistencia
- **requests** — librería HTTP usada en el cliente de prueba

## Estructura

```
challenge-5-log-collector/
├── server.py           # Servidor Flask con los endpoints de la API
├── cliente.py          # Cliente de prueba que genera y envía logs
├── tokens.example.json # Ejemplo de configuración de tokens
└── README.md
```

## Setup

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# Instalar dependencias
pip install flask requests

# Configurar tokens
cp tokens.example.json tokens.json
# Editar tokens.json con los tokens reales

# Iniciar el servidor
python server.py
```

## Endpoints

### `POST /logs`

Recibe uno o múltiples logs. Requiere token de autenticación.

**Header requerido:**
```
Authorization: Token <tu-token>
```

**Body (objeto único):**
```json
{
  "timestamp": "2024-01-15T10:30:00+00:00",
  "service": "service_alpha",
  "severity": "ERROR",
  "message": "Timeout inesperado."
}
```

**Body (lista de logs):**
```json
[
  { "timestamp": "...", "service": "service_alpha", "severity": "INFO", "message": "Todo bien." },
  { "timestamp": "...", "service": "service_beta",  "severity": "ERROR", "message": "Algo falló." }
]
```

**Respuestas:**
| Código | Descripción |
|--------|-------------|
| `201`  | Logs guardados correctamente |
| `401`  | Token inválido o ausente |

---

### `GET /logs`

Consulta los logs almacenados. Todos los parámetros son opcionales.

**Query parameters:**
| Parámetro | Descripción |
|-----------|-------------|
| `severity` | Filtra por nivel: `INFO`, `DEBUG`, `WARNING`, `ERROR` |
| `timestamp_start` | Logs con timestamp mayor o igual a este valor |
| `timestamp_end` | Logs con timestamp menor o igual a este valor |
| `received_at_start` | Logs recibidos por el servidor desde esta fecha |
| `received_at_end` | Logs recibidos por el servidor hasta esta fecha |

**Ejemplo:**
```
GET /logs?severity=ERROR&timestamp_start=2024-01-15T00:00:00Z
```

**Respuesta `200`:**
```json
[
  {
    "id": 1,
    "timestamp": "2024-01-15T10:30:00+00:00",
    "service": "service_alpha",
    "severity": "ERROR",
    "message": "Timeout inesperado.",
    "received_at": "2024-01-15T10:30:01+00:00"
  }
]
```

## Cliente de prueba

```bash
python cliente.py
```

Genera 5 logs aleatorios y los envía al servidor. Muestra el código de respuesta y el body JSON en consola.

---

## Conceptos clave

Ver [CONCEPTS.md](CONCEPTS.md) para una explicación detallada de los conceptos técnicos aplicados en este proyecto.
