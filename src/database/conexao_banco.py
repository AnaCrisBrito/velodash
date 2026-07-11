import sqlite3

conexao = sqlite3.connect('velodash.db')

cursor = conexao.cursor()



cursor.execute("PRAGMA foreign_keys = ON;")

table_categorias = '''
CREATE TABLE IF NOT EXISTS CATEGORIAS (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL
);
'''

table_registros = '''
CREATE TABLE IF NOT EXISTS REGISTROS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT NOT NULL,
    valor_unitario NUMERIC NOT NULL,
    cliente TEXT NOT NULL,
    responsavel TEXT NOT NULL, 
    quantidade INTEGER NOT NULL,
    valor_total NUMERIC NOT NULL,

    FOREIGN KEY (categoria_id) REFERENCES CATEGORIAS(id)
);
'''

cursor.execute(table_categorias)
cursor.execute(table_registros)

conexao.commit()
conexao.close()
