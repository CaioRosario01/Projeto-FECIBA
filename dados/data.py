
import sqlite3
import pandas as pd

#1. conecta/cria banco SQLite
conn = sqlite3.connect('database.db')

# 2. lê o CSV (SEU ARQUIVO REAL)
df = pd.read_csv("praias.csv")

# 3. salva no banco
df.to_sql("medicoes", conn, if_exists="replace", index=False)

print("Banco criado com sucesso")