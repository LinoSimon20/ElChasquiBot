import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PORT = int(os.getenv("PORT", 8000))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN no esta definido en el archivo .env")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN no esta definido en el archivo .env")