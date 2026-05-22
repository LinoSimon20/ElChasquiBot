from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from dotenv import load_dotenv
from cooldown import verificar_cooldown

import os, logging, time

from database import (
    iniciar_database,
    guardar_usuario,
    obtener_usuario,
    eliminar_usuario
)

from github_api import (
    github_user_exists,
    get_user_comentarios,
    get_issues_asignados,
    get_user_prs_mergeados
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True
)

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

async def enviar_mensajes_largos(
    update,
    text,
    limit=4000
):

    partes = []

    while len(text) > limit:

        indice_dividido = text.rfind(
            "\n",
            0,
            limit
        )

        if indice_dividido == -1:
            indice_dividido = limit

        partes.append(
            text[:indice_dividido]
        )

        text = text[indice_dividido:]

    partes.append(text)

    for parte in partes:

        await update.message.reply_text(
            parte
        )

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

def main():

    iniciar_database()

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start)
    )

    app.add_handler(
        CommandHandler(
            "vincular",
            vincular
        )
    )

    app.add_handler(
        CommandHandler(
            "mis_comentarios",
            mis_comentarios
        )
    )

    app.add_handler(
        CommandHandler(
            "mis_issues",
            mis_issues
        )
    )

    app.add_handler(
        CommandHandler(
            "mi_estado",
            mi_estado
        )
    )

    app.add_handler(
        CommandHandler(
            "ayuda",
            ayuda
        )
    )

    app.add_handler(
        CommandHandler(
            "desvincular",
            desvincular
        )
    )

    app.add_error_handler(
        manejar_error
    )

    logging.info("Iniciando ElChasquiBot...")
    time.sleep(1)
    logging.info("ElChasquiBot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()