import asyncio

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler
)

from bot.services.config import BOT_TOKEN

from bot.handlers.start import start
from bot.handlers.vincular import vincular
from bot.handlers.comentarios import mis_comentarios
from bot.handlers.issues import mis_issues
from bot.handlers.estado import mi_estado
from bot.handlers.ayuda import ayuda
from bot.handlers.desvincular import desvincular
from bot.utils.logger import manejar_error
from bot.db.database import iniciar_database
from bot.web.server import iniciar_web_server

import logging, time

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True
)

async def main():

    iniciar_database()

    await iniciar_web_server()

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start)
    )

    app.add_handler(
        CommandHandler(
            "vincular",
            vincular
        )
    )

    app.add_handler(
        CommandHandler(
            "mis_comentarios",
            mis_comentarios
        )
    )

    app.add_handler(
        CommandHandler(
            "mis_issues",
            mis_issues
        )
    )

    app.add_handler(
        CommandHandler(
            "mi_estado",
            mi_estado
        )
    )

    app.add_handler(
        CommandHandler(
            "ayuda",
            ayuda
        )
    )

    app.add_handler(
        CommandHandler(
            "desvincular",
            desvincular
        )
    )

    app.add_error_handler(
        manejar_error
    )

    logging.info("Iniciando ElChasquiBot...")

    try:
        await app.initialize()
        await app.start()
        logging.info("ElChasquiBot iniciado correctamente.")
        await app.updater.start_polling()
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        logging.info("ElChasquiBot detenido.")

if __name__ == "__main__":
    asyncio.run(main())