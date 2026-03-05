import sqlite3

def conectar():
	return sqlite3.connect("dados.db") 


def criar_tabelas():
	conn = conectar() 
	cursor = conn.cursor() 
	
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS produtos (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nome TEXT NOT NULL,
	quantiade INTEGER NOT NULL
	)
	""")
	
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS movimentacoes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	produto_id INTEGER,
	tipo TEXT,
	quantidade INTEGER,
	responsavel TEXT,
	data DATATIME DEFAULT CURRENT_TIMESTAMP 
	)
	""")
	
	conn.commit()
	conn.close()
	
	
