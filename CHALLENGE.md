# Challenge 5 — Log Collector API

## Consigna

Construir una **API REST** en Python usando **Flask** que actúe como servidor centralizado de logs. La API debe:

### Funcionalidad requerida

#### Endpoint `POST /logs`
- Recibir logs enviados por distintos servicios/clientes
- Validar autenticación mediante un **token Bearer** en el header `Authorization`
- Aceptar tanto un **objeto único** como una **lista** de logs en el cuerpo JSON
- Guardar cada log en una base de datos **SQLite** con los campos:
  - `timestamp` — fecha y hora del evento (enviada por el cliente)
  - `service` — nombre del servicio que genera el log
  - `severity` — nivel de severidad (`INFO`, `DEBUG`, `WARNING`, `ERROR`)
  - `message` — mensaje descriptivo del evento
  - `received_at` — timestamp generado en el servidor al momento de recibir el log
- Retornar `201 Created` si los logs se guardaron correctamente
- Retornar `401 Unauthorized` si el token es inválido

#### Endpoint `GET /logs`
- Retornar todos los logs almacenados en formato JSON
- Soportar **filtros opcionales** mediante query parameters:
  - `timestamp_start` / `timestamp_end` — rango de tiempo del evento
  - `severity` — filtrar por nivel de severidad
  - `received_at_start` / `received_at_end` — rango de tiempo de recepción en el servidor

### Cliente de prueba
- Implementar un script cliente (`cliente.py`) que:
  - Genere logs aleatorios con datos de prueba
  - Los envíe al servidor usando el header de autenticación correcto
  - Muestre en consola el código de respuesta y el body JSON retornado

### Requisitos técnicos
- Lenguaje: **Python 3**
- Framework: **Flask**
- Base de datos: **SQLite** (sin ORM, usando `sqlite3` nativo)
- Los tokens válidos deben cargarse desde un archivo externo `tokens.json`
- Soporte para múltiples servicios con tokens distintos
