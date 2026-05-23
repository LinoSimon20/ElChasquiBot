from telegram import Update
from telegram.ext import ContextTypes

from github.client import github_user_exists
from bot.db.database import (
    obtener_usuario,
    guardar_usuario
)
from bot.utils.logger import log_accion

async def vincular(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    usuario_existente = obtener_usuario(telegram_id)

    if usuario_existente:

        await update.message.reply_text(
            f"Ya tienes una cuenta vinculada: {usuario_existente}.\n"
        )

        return

    if len(context.args) != 1:

        await update.message.reply_text(
            "Uso:\n/vincular usuarioGithub"
        )

        return

    usuario = context.args[0]

    exists = await github_user_exists(
        usuario
    )

    if not exists:

        await update.message.reply_text(
            f"El usuario {usuario} no existe."
        )

        return

    guardar_usuario(
        telegram_id,
        usuario
    )

    log_accion(usuario, "/vincular")

    await update.message.reply_text(
        f"Realizado. Tu usuario {usuario}, ha sido vinculado :).\n"
        "Ahora puedes usar /mis_comentarios :)"
    )