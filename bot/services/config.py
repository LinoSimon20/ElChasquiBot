import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PORT = int(os.getenv("PORT", 8080))
APP_URL = os.getenv("APP_URL")

WEEBHOOK_PATH = "/webhook"

WEEBHOOK_URL = (
    f"{APP_URL}{WEEBHOOK_PATH}"
    if APP_URL
    else None
)

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN no esta definido en el archivo .env")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN no esta definido en el archivo .env")

if not APP_URL:
    raise ValueError("APP_URL no esta definido en el archivo .env")