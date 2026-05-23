# ElChasquiBot

## Descripción

ElChasquiBot es un bot de Telegram orientado a colaboradores de GitHub. Su objetivo es permitir que los usuarios consulten rápidamente su actividad reciente relacionada con issues y comentarios realizados en proyectos open source directamente desde Telegram.

El bot funciona vinculando un usuario de GitHub con una cuenta de Telegram y posteriormente permitiendo consultar información pública asociada a dicho usuario.

---

## Características principales

* Vinculación de cuenta GitHub mediante nombre de usuario
* Consulta de comentarios recientes realizados en issues
* Consulta de issues asignadas al usuario
* Consulta de estado de GitHub del usuario
    * Issues asignadas
    * Comentarios
    * Pull Requests mergeados
* Sistema multiusuario
* Cooldown para evitar spam
* Manejo automático de mensajes largos
* Integración con GitHub API
* Persistencia local mediante SQLite

---

## Comandos disponibles

| Comando               | Descripción                                        |
| --------------------- | -------------------------------------------------- |
| `/start`              | Mensaje de bienvenida                              |
| `/vincular <usuario>` | Vincula una cuenta GitHub                          |
| `/mis_comentarios`    | Muestra comentarios recientes realizados en issues |
| `/mis_issues`         | Muestra issues asignadas al usuario                |
| `/mi_estado`          | Muestra el estado de GitHub del usuario            |
| `/ayuda`              | Lista de comandos disponibles                      |
| `/desvincular`        | Elimina la vinculación actual                      |

---

## Tecnologías utilizadas

* Python 3
* python-telegram-bot
* SQLite
* GitHub REST API

---

## Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/LinoSimon20/ElChasquiBot
cd ElChasquiBot
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Asegúrate de usar Python 3.10+

### 4. Configurar variables de entorno

Crear archivo `.env`

```env
BOT_TOKEN=TU_TOKEN
GITHUB_TOKEN=TU_TOKEN_GITHUB
```

### 5. Ejecutar bot

```bash
python3 bot.py
```

---

## Estructura general del proyecto

```txt
ElChasquiBot/
├── bot.py
├── requirements.txt
├── .env.example
├── CHANGELOG.md
│
├── bot/
│   ├── handlers/
│   ├── utils/
│   ├── services/
│   └── db/
│
├── github/
│   └── client.py
│
├── docs/
│   ├── arquitectura.md
│   ├── casos-de-uso.md
│   ├── requerimientos.md
│   └── seguridad.md
│
└── users.db
```
---

## Licencia

Proyecto desarrollado con fines educativos y de aprendizaje.

---

# Posibles mejoras futuras

* Caché avanzada
* Base de datos PostgreSQL
* Deploy en VPS cloud
* Sistema de notificaciones
* Dockerización
* Panel web administrativo
* Integración con organizaciones GitHub