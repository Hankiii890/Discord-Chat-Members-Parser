import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Определяем переменные окружения
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def connect_to_db():
    connect = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connect


def table_addition():
    with open('tables.sql') as f:
        sql = f.read()
    connect = connect_to_db()
    cur = connect.cursor()
    cur.execute(sql)
    connect.commit()
    cur.close()


if __name__ == '__main__':
    table_addition()