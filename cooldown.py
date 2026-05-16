import time

ULTIMO_USO = {}

TIEMPO_COOLDOWN = 15


def verificar_cooldown(user_id):

    ahora = time.time()

    ultima_vez = ULTIMO_USO.get(user_id)

    if ultima_vez:

        restante = (
            TIEMPO_COOLDOWN
            - (ahora - ultima_vez)
        )

        if restante > 0:
            return int(restante)

    ULTIMO_USO[user_id] = ahora

    return 0