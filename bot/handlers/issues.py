from telegram import Update
from telegram.ext import ContextTypes

from github.client import get_issues_asignados
from bot.db.database import obtener_usuario
from bot.utils.cooldown import verificar_cooldown
from bot.utils.logger import log_accion
from bot.utils.mensajes import enviar_mensajes_largos

async def mis_issues(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    cooldown = verificar_cooldown(
        telegram_id,
        "/mis_issues"
    )

    if cooldown > 0:

        await update.message.reply_text(
            f"Espera {cooldown}s antes de usar este comando nuevamente."
        )

        return

    usuario = obtener_usuario(
        telegram_id
    )

    if not usuario:

        await update.message.reply_text(
            "Primero usa /vincular"
        )

        return

    log_accion(usuario, "/mis_issues")

    issues = await get_issues_asignados(
        usuario
    )

    if issues == "rate_limit":
        
        await update.message.reply_text(
            "GitHub rate limit alcanzado, intentalo nuevamente mas tarde."
        )
        
        return

    if issues is None:

        await update.message.reply_text(
            "Error de GitHub API"
        )

        return

    if not issues:

        await update.message.reply_text(
            "No tienes issues asignadas :("
        )

        return

    mensaje = "🐛 Issues asignadas:\n\n"

    contador_issues = 0

    for issue in issues:

        mensaje += (
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📦 Repo: {issue['repo']}\n\n"
            f"🐛 {issue['title']}\n\n"
            f"🔗 {issue['url']}\n\n"
        )

        contador_issues += 1

    mensaje += (
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📊 Total de issues asignadas: "
        f"{contador_issues}"
    )

    await enviar_mensajes_largos(
        update,
        mensaje
    )