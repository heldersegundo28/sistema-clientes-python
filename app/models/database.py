"""Módulo de gerenciamento de banco de dados SQLite."""

import sqlite3
from typing import List, Tuple
from app.config import DATABASE_PATH


def conn() -> sqlite3.Connection:
    """Estabelece conexão com o banco de dados.
    
    Returns:
        sqlite3.Connection: Conexão com o banco de dados.
    """
    return sqlite3.connect(DATABASE_PATH)


def init_db() -> None:
    """Inicializa o banco de dados e cria tabelas se necessário.
    
    Raises:
        Exception: Se houver erro ao inicializar o banco.
    """
    try:
        c = conn()
        c.execute('''
            CREATE TABLE IF NOT EXISTS clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefone TEXT NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.commit()
        c.close()
    except sqlite3.Error as err:
        raise Exception(f'Erro ao inicializar banco: {err}') from err


def close_connection(conn_obj: sqlite3.Connection) -> None:
    """Fecha a conexão com o banco de dados.
    
    Args:
        conn_obj: Conexão a ser fechada.
    """
    if conn_obj:
        conn_obj.close()