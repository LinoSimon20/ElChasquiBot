from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.cooldown import verificar_cooldown
from bot.utils.logger import log_accion

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    usuario = (
        update.effective_user.username
        or str(update.effective_user.id)
    )

    log_accion(usuario, "/start")

    await update.message.reply_text(
        "¡Hola!.\nSoy ChasquiBot, tu mensajero que recopilara todos los mensajes que dejaste en los Issues de proyectos de GitHub en los que colaboras.\n\n"
        "Para comenzar:\n\n"
        "- Registra tu usuario de github, escribe:\n"
        "/vincular usuario\n\n"
        "Para obtener los mensajes recopilados de los Issues de tus proyectos de GitHub escribe:\n"
        "/mis_comentarios\n\n"
        "Para obtener las Issues asignadas escribe:\n"
        "/mis_issues\n\n"
        "Para obtener tu estado escribe:\n"
        "/mi_estado\n\n"
        "Para mas informacion escribe:\n"
        "/ayuda"
    )