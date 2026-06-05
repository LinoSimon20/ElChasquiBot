import logging
from aiohttp import web
from bot.services.config import PORT

logger = logging.getLogger(__name__)

async def salud(request):
    return web.Response(text="OK", status=200)

async def iniciar_web_server():
    app = web.Application()
    app.router.add_get("/", salud)
    app.router.add_get("/health", salud)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Servidor web corriendo en puerto {PORT}")