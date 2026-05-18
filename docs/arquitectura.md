# Arquitectura general

## Componentes principales

### bot.py

Contiene:

* comandos Telegram
* lógica principal
* manejo de mensajes

### github_api.py

Contiene:

* integración con GitHub API
* consultas HTTP
* procesamiento de respuestas

### cache.py

Contiene:

* almacenamiento temporal de consultas recientes
* reducción de llamadas innecesarias a GitHub API
* mejora de rendimiento y tiempos de respuesta

### cooldown.py

Contiene:

* control de frecuencia de comandos
* prevención de spam
* limitación temporal de solicitudes por usuario

### database.py

Contiene:

* persistencia SQLite
* almacenamiento de usuarios vinculados

# Base de datos

## Tabla usuarios

| Campo       | Tipo    |
| ----------- | ------- |
| telegram_id | INTEGER |
| github_user | TEXT    |

---