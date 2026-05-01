
import psycopg2
from config import DB_CONFIG

def get_connection():
    # тут подключаемся к PostgreSQL и возвращаем соединение
    return psycopg2.connect(**DB_CONFIG)
