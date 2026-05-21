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
    get_issues_asignados
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logging.getLogger("httpx").setLevel(logging.WARNING)

def log_accion(usuario, accion):
    logging.info(
        f"{accion} ejecutada por: {usuario}"
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

    await update.message.reply_text(
        "¡Hola!.\nSoy ChasquiBot, tu mensajero que recopilara todos los mensajes que dejaste en los Issues de proyectos de GitHub en los que colaboras.\n\n"
        "Para comenzar:\n\n"
        "- Registra tu usuario de github, escribe:\n"
        "/vincular usuario\n\n"
        "Para obtener los mensajes recopilados de los Issues de tus proyectos de GitHub escribe:\n"
        "/mis_comentarios\n\n"
        "Para obtener las Issues asignadas escribe:\n"
        "/mis_issues\n\n"
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
    update.effective_user.id
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
    
    contador_mensajes = 0
    
    for item in comentarios:

        mensaje = (       
            f"📦 Repo: {item['repo']}\n\n"
            f"📝 {item['title']}\n\n"
            f"💬 {item['comment']}\n\n"
            f"🔗 {item['url']}"
        )

        contador_mensajes +=1

        await update.message.reply_text(
            mensaje
        )

    await update.message.reply_text(
        f"Tienes un total de: {contador_mensajes} comentarios recientes."
    )

async def mis_issues(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    cooldown = verificar_cooldown(telegram_id)

    if cooldown > 0:

        await update.message.reply_text(
            f"Espera {cooldown}s antes de usar este comando nuevamente."
        )

        return

    usuario = obtener_usuario(
        telegram_id
    )

    log_accion(usuario, "/mis_issues")

    if not usuario:

        await update.message.reply_text(
            "Primero usa /vincular"
        )

        return

    issues = await get_issues_asignados(
        usuario
    )

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

    mensaje = "Issues asignadas:\n\n"

    contador = 0

    for issue in issues:

        mensaje += (
            f"📦 {issue['repo']}\n"
            f"🐛 {issue['title']}\n"
            f"🔗 {issue['url']}\n\n"
        )

        contador += 1

    await enviar_mensajes_largos(
        update,
        mensaje
    )

    await update.message.reply_text(
        f"Tienes un total de: {contador} issues asignadas."
    )

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

    await update.message.reply_text(
        "Ayuda de ChasquiBot:\n\n"
        "ChasquiBot es un bot que te ayuda a gestionar los mensajes que dejaste en los issues de tus proyectos de GitHub.\n\n"
        "- Para registrar tu usuario de github, escribe:\n"
        "/vincular usuarioGithub\n\n"
        "- Para obtener los mensajes recopilados de los Issues de tus proyectos de GitHub escribe:\n"
        "/mis_comentarios\n\n"
        "- Para obtener las Issues asignadas escribe:\n"
        "/mis_issues\n\n"
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

    logging.info("Iniciando ElChasquiBot...")
    time.sleep(1)
    logging.info("ElChasquiBot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()