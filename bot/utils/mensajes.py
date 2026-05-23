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