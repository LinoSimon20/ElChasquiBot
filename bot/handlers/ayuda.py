from telegram import Update
from telegram.ext import ContextTypes

from bot.db.database import obtener_usuario
from bot.utils.logger import log_accion

async def ayuda(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    usuario = obtener_usuario(
        telegram_id
    ) or "Desconocido"

    log_accion(usuario, "/ayuda")

    await update.message.reply_text(
        "Ayuda de ChasquiBot:\n\n"
        "ChasquiBot es un bot que te ayuda a gestionar los mensajes que dejaste en los issues de tus proyectos de GitHub.\n\n"
        "- Para registrar tu usuario de github, escribe:\n"
        "/vincular usuarioGithub\n\n"
        "- Para obtener los mensajes recopilados de los Issues de tus proyectos de GitHub escribe:\n"
        "/mis_comentarios\n\n"
        "- Para obtener las Issues asignadas escribe:\n"
        "/mis_issues\n\n"
        "- Para obtener tu estado escribe:\n"
        "/mi_estado\n\n"
        "- Para desvincular tu cuenta de GitHub escribe:\n"
        "/desvincular\n\n"
        "¡Gracias por usar ChasquiBot!\n"
        "El bot se encuentra en una fase experimental, cualquier sugerencia es bienvenida. "
        "Contactame cualquier duda o sugerencia :)\n"
        "GitHub: https://github.com/LinoSimon20\n"
        "Telegram: https://t.me/LinoSimon"
    )