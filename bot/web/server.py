import logging

from aiohttp import web
from telegram import Update

from bot.services.config import (
    PORT,
    WEBHOOK_PATH
)

logger = logging.getLogger(__name__)

telegram_app = None


async def salud(request):

    return web.Response(
        text="OK",
        status=200
    )


async def manejar_webhook(request):

    data = await request.json()

    update = Update.de_json(
        data,
        telegram_app.bot
    )

    await telegram_app.update_queue.put(update)

    return web.Response(status=200)


async def iniciar_web_server(app_telegram):

    global telegram_app

    telegram_app = app_telegram

    app = web.Application()

    app.router.add_get("/", salud)
    app.router.add_get("/health", salud)

    app.router.add_post(
        WEBHOOK_PATH,
        manejar_webhook
    )

    runner = web.AppRunner(app)

    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        PORT
    )

    await site.start()

    logger.info(
        f"Servidor web corriendo en puerto {PORT}"
    )
