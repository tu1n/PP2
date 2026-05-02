import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "snake_game",
    "user":   "postgres",
    "password": "tu1n@2007"
}

def get_connection():
    """Просто подключаемся к базе"""
    return psycopg2.connect(**DB_CONFIG)


def create_tables():
    """Создаём таблицы если их ещё нет"""
    conn = get_connection()
    cur = conn.cursor()

    # Таблица игроков
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id       SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    # Таблица игровых сессий
    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id            SERIAL PRIMARY KEY,
            player_id     INTEGER REFERENCES players(id),
            score         INTEGER   NOT NULL,
            level_reached INTEGER   NOT NULL,
            played_at     TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_or_create_player(username):
    """Находим игрока по имени, или создаём нового"""
    conn = get_connection()
    cur = conn.cursor()

    # Попробуем найти
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()

    if row:
        player_id = row[0]
    else:
        # Такого нет — создаём
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return player_id


def save_game_result(player_id, score, level):
    """Сохраняем результат после окончания игры"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
        (player_id, score, level)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_personal_best(player_id):
    """Лучший результат этого игрока"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
        (player_id,)
    )
    result = cur.fetchone()[0]

    cur.close()
    conn.close()
    return result or 0  # если ни одной игры — возвращаем 0


def get_top10():
    """Топ-10 игроков всех времён"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC
        LIMIT 10
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows