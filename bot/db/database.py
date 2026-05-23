import sqlite3

NOMBRE_DB = "users.db"

def iniciar_database():
    conn = sqlite3.connect(NOMBRE_DB)

    conn.execute(
        "PRAGMA journal_mode=WAL"
    )

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        github_username TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def guardar_usuario(telegram_id, github_username):
    conn = sqlite3.connect(NOMBRE_DB)

    conn.execute("""
    INSERT OR REPLACE INTO users
    (telegram_id, github_username)
    VALUES (?, ?)
    """, (telegram_id, github_username))

    conn.commit()
    conn.close()

def obtener_usuario(telegram_id):
    conn = sqlite3.connect(NOMBRE_DB)

    cursor = conn.execute("""
    SELECT github_username
    FROM users
    WHERE telegram_id = ?
    """, (telegram_id,))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None

def eliminar_usuario(telegram_id):
    conn = sqlite3.connect(NOMBRE_DB)

    conn.execute("""
    DELETE FROM users
    WHERE telegram_id = ?
    """, (telegram_id,))

    conn.commit()
    conn.close()