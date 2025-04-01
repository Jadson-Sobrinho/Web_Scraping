import sqlite3

db_path = "backend\\database\\data.db"


def get_db_connection():
    conn = sqlite3.connect(db_path, check_same_thread=False)  # Permite acesso entre threads
    conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelo nome
    return conn
