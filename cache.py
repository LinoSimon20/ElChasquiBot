import time

CACHE = {}

CACHE_DURATION = 60


def get_cache(key):

    data = CACHE.get(key)

    if not data:
        return None

    if time.time() > data["expires"]:
        del CACHE[key]
        return None

    return data["value"]


def set_cache(key, value):

    CACHE[key] = {
        "value": value,
        "expires": time.time() + CACHE_DURATION
    }