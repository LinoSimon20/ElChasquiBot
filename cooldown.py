import time

ULTIMO_USO = {}

TIEMPO_COOLDOWN = 15


def verificar_cooldown(
    user_id,
    comando
):

    clave = (
        user_id,
        comando
    )

    ahora = time.time()

    ultima_vez = ULTIMO_USO.get(clave)

    if ultima_vez:

        restante = (
            TIEMPO_COOLDOWN
            - (ahora - ultima_vez)
        )

        if restante > 0:
            return int(restante)

    ULTIMO_USO[clave] = ahora

    return 0