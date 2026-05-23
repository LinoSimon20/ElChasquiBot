from telegram import Update
from telegram.ext import ContextTypes

from bot.db.database import eliminar_usuario
from bot.db.database import obtener_usuario
from bot.utils.logger import log_accion

async def desvincular(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if len(context.args) != 1:

        await update.message.reply_text(
            "Uso:\n/desvincular usuarioGitHub"
        )

        return

    telegram_id = update.effective_user.id

    usuario = obtener_usuario(
        telegram_id
    )

    if not usuario:

        await update.message.reply_text(
            "No tienes ninguna cuenta vinculada."
        )

        return
    
    usuario_ingresado = context.args[0]

    if usuario_ingresado != usuario:

        await update.message.reply_text(
            "El usuario ingresado no coincide con el usuario vinculado."
        )

        return

    log_accion(usuario, "/desvincular")

    eliminar_usuario(telegram_id)

    await update.message.reply_text(
        "Realizado. Tu cuenta ha sido desvinculada con exito! :)."
    )