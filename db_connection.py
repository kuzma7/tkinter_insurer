import sqlite3


# Подключение к базе данных SQLite
def connect_db():
    conn = sqlite3.connect('data_base.db')  # Имя базы данных
    return conn
