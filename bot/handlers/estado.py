import asyncio

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

    cooldown = verificar_cooldown(telegram_id, "/mi_estado")

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

    issues, comentarios, prs = await asyncio.gather(
        get_issues_asignados(usuario),
        get_user_comentarios(usuario),
        get_user_prs_mergeados(usuario)
    )

    if "rate_limit" in (issues, comentarios, prs):
        await update.message.reply_text(
            "GitHub rate limit alcanzado, intentalo nuevamente mas tarde."
        )
        return

    if None in (issues, comentarios, prs):
        await update.message.reply_text(
            "GitHub no respondió correctamente, intentalo más tarde."
        )
        return

    mensaje = (
        f"🏆 Estado de {usuario}:\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🐛 Issues asignadas: {len(issues or [])}\n\n"
        f"💬 Comentarios: {len(comentarios or [])}\n\n"
        f"🔀 Pull Requests mergeados: {len(prs or [])}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
    )

    await update.message.reply_text(mensaje)