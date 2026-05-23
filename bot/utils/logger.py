import logging
from telegram.ext import ContextTypes

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)

def log_accion(usuario, accion):

    usuario = usuario or "Desconocido"

    logging.info(
        f"{accion} ejecutada por: {usuario}"
    )

async def manejar_error(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    
    usuario = "Desconocido"

    if update and hasattr(update, "effective_user"):

        if update.effective_user:

            usuario = (
                update.effective_user.username
                or str(update.effective_user.id)
            )

    logging.error(
        "━━━━━━━━━━━━━━━━━━━━"
    )

    logging.error(
        f"Error detectado para usuario: {usuario}"
    )

    logging.error(
        f"Error: {context.error}"
    )

    logging.error(
        "Traceback completo:",
        exc_info=context.error
    )

    logging.error(
        "━━━━━━━━━━━━━━━━━━━━"
    )