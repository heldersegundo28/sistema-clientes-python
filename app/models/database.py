import sqlite3
def conn():
    return sqlite3.connect('clientes.db')
def init_db():
    c=conn()
    c.execute('''CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,email TEXT UNIQUE,telefone TEXT)''')
    c.commit(); c.close()