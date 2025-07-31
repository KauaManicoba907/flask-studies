# Aqui estão todas as consultas para o banco de dados
# que serão utilizadas no projeto todolist.

import sqlite3
from main import app

con = sqlite3.connect('todolist.db')
cur = con.cursor()

# Tabela de usuários
cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    telefone TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    como_conheceu TEXT NOT NULL
)
""")

# Tabela de categorias
cur.execute("CREATE TABLE IF NOT EXISTS categorias (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL UNIQUE, descricao TEXT)")

# Tabela de tarefas
cur.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    data_criacao TEXT NOT NULL,
    data_conclusao TEXT,
    status TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
)
""")



con.commit()
con.close()

