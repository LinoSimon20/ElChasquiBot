from telegram import Update
from telegram.ext import ContextTypes

from github.client import get_user_comentarios
from bot.db.database import obtener_usuario
from bot.utils.cooldown import verificar_cooldown
from bot.utils.logger import log_accion
from bot.utils.mensajes import enviar_mensajes_largos

async def mis_comentarios(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    cooldown = verificar_cooldown(
        telegram_id,
        "/mis_comentarios"
    )

    if cooldown > 0:

        await update.message.reply_text(
           f"Espera {cooldown}s antes "
           "de usar este comando nuevamente."
        )

        return

    usuario = obtener_usuario(telegram_id)

    if not usuario:

        await update.message.reply_text(
            "Primero usa /vincular para ver tus mensajes de GitHub."
        )

        return

    comentarios = await get_user_comentarios(
        usuario
    )

    log_accion(usuario, "/mis_comentarios")

    if comentarios == "rate_limit":
        
        await update.message.reply_text(
            "GitHub rate limit alcanzado, intentalo nuevamente mas tarde."
        )
        
        return

    if comentarios is None:
        
        await update.message.reply_text(
            "GitHub no respondió, intentalo nuevamente mas tarde."
        )
        
        return

    if not comentarios:

        await update.message.reply_text(
            "No encontré comentarios recientes."
        )

        return
    
    mensaje = "💬 Comentarios recientes:\n\n"

    contador_comentarios = 0

    for item in comentarios:

        mensaje += (
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📦 Repo: {item['repo']}\n\n"
            f"📝 {item['title']}\n\n"
            f"💬 {item['comment']}\n\n"
            f"🔗 {item['url']}\n\n"
        )

        contador_comentarios += 1

    mensaje += (
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📊 Total de comentarios: "
        f"{contador_comentarios}"
    )

    await enviar_mensajes_largos(
        update,
        mensaje
    )