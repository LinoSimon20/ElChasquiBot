from telegram import Update
from telegram.ext import ContextTypes

from github.client import (
    get_user_comentarios,
    get_issues_asignados,
    get_user_prs_mergeados
)
from bot.db.database import obtener_usuario
from bot.utils.cooldown import verificar_cooldown
from bot.utils.logger import log_accion

async def mi_estado(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    cooldown = verificar_cooldown(
        telegram_id,
        "/mi_estado"
    )

    if cooldown > 0:

        await update.message.reply_text(
            f"Espera {cooldown}s antes de usar este comando nuevamente."
        )

        return

    usuario = obtener_usuario(telegram_id)

    if not usuario:

        await update.message.reply_text(
            "Primero usa /vincular para ver tu estado."
        )

        return

    log_accion(usuario, "/mi_estado")

    issues = await get_issues_asignados(usuario)

    if issues == "rate_limit":

        await update.message.reply_text(
            "GitHub rate limit alcanzado, intentalo nuevamente mas tarde."
        )

        return

    if issues is None:

        await update.message.reply_text(
            "GitHub no respondió al obtener las issues."
        )

        return

    comentarios = await get_user_comentarios(usuario)

    if comentarios == "rate_limit":

        await update.message.reply_text(
            "GitHub rate limit alcanzado, intentalo nuevamente mas tarde."
        )

        return

    if comentarios is None:

        await update.message.reply_text(
            "GitHub no respondió al obtener los comentarios."
        )

        return

    prs = await get_user_prs_mergeados(usuario)

    if prs == "rate_limit":

        await update.message.reply_text(
            "GitHub rate limit alcanzado, intentalo nuevamente mas tarde."
        )

        return

    if prs is None:

        await update.message.reply_text(
            "GitHub no respondió al obtener los pull requests."
        )

        return

    total_issues = len(issues)
    total_comentarios = len(comentarios)
    total_prs = len(prs)

    mensaje = (
        f"🏆 Estado de {usuario}:\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🐛 Issues asignadas: {total_issues}\n\n"
        f"💬 Comentarios: {total_comentarios}\n\n"
        f"🔀 Pull Requests mergeados: {total_prs}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    await update.message.reply_text(mensaje)