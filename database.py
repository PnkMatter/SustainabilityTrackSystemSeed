# database.py
import sqlite3
import pandas as pd

# Garante que a pasta exista mesmo se o deploy apagar tudo

def init_db():
    conn = sqlite3.connect("data/projetos.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            escopo1 REAL,
            escopo2 REAL,
            escopo3 REAL,
            data_inicio DATE,
            data_fim DATE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS real_values (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sigla TEXT,
            fabrica TEXT,
            pais TEXT,
            regiao TEXT,
            ano INTEGER,
            mes INTEGER,
            emissao_total integer,
            energia_gerada_local INTEGER,
            energia_verde_comprada INTEGER,  
            escopo1 REAL,
            escopo2 REAL,
            escopo3 REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_project(nome, tipo, escopo1, escopo2, escopo3, data_inicio, data_fim):
    conn = sqlite3.connect("data/projetos.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO projetos (nome, tipo, escopo1, escopo2, escopo3, data_inicio, data_fim)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, tipo, escopo1, escopo2, escopo3, data_inicio, data_fim))
    conn.commit()
    conn.close()

def get_all_projects():
    conn = sqlite3.connect("data/projetos.db")
    df = pd.read_sql_query("SELECT nome, tipo, escopo1 as 'Escopo 1', escopo2 as 'Escopo 2', escopo3 as 'Escopo 3', data_inicio as 'Data Início', data_fim as 'Data Fim' FROM projetos", conn)
    conn.close()
    return df

def insert_real_values(sigla, fabrica, pais, regiao, ano, mes, emissao_total, energia_gerada_local, energia_verde_comprada, escopo1, escopo2, escopo3):
    conn = sqlite3.connect("data/projetos.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO real_values (sigla, fabrica, pais, regiao, ano, mes, emissao_total, energia_gerada_local, energia_verde_comprada, escopo1, escopo2, escopo3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sigla, fabrica, pais, regiao, ano, mes, emissao_total, energia_gerada_local, energia_verde_comprada, escopo1, escopo2, escopo3))
    conn.commit()
    conn.close()

def get_all_emissoes():
    conn = sqlite3.connect("data/projetos.db")
    df = pd.read_sql_query("SELECT * FROM emissoes_mensais", conn)
    conn.close()
    return df

def get_monthly_real_emissions():
    conn = sqlite3.connect("data/projetos.db")
    df = pd.read_sql_query("""
        SELECT ano, mes, SUM(escopo1) AS escopo1, SUM(escopo2) AS escopo2, SUM(escopo3) AS escopo3
        FROM real_values
        GROUP BY ano, mes
        ORDER BY ano, mes
    """, conn)
    conn.close()
    return df

def get_monthly_project_reductions():
    conn = sqlite3.connect("data/projetos.db")
    df = pd.read_sql_query("""
        SELECT data_inicio, data_fim, escopo1, escopo2, escopo3
        FROM projetos
    """, conn)
    conn.close()

    # Expande projetos por mês
    rows = []
    for _, row in df.iterrows():
        data_inicio = pd.to_datetime(row["data_inicio"])
        data_fim = pd.to_datetime(row["data_fim"])
        meses = pd.date_range(data_inicio, data_fim, freq='MS')  # Início do mês
        for mes in meses:
            rows.append({
                "ano": mes.year,
                "mes": mes.month,
                "escopo1": row["escopo1"] / len(meses),
                "escopo2": row["escopo2"] / len(meses),
                "escopo3": row["escopo3"] / len(meses),
            })

    return pd.DataFrame(rows)
