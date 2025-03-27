import sqlite3
import pandas as pd

relatorio_cadop_path = ("C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\input\\Relatorio_cadop.csv")
operadoras_ativas_path = ("C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\output\\4T2024.csv")

df_relatorio_cadop = pd.read_csv(relatorio_cadop_path, encoding='utf-8-sig', sep=';')
df_operadoras_ativas = pd.read_csv(operadoras_ativas_path, encoding='utf-8-sig', sep=';')

conn = sqlite3.connect(":memory:")

df_relatorio_cadop.to_sql("Relatorio_cadop", conn, index=False, if_exists="replace")
df_operadoras_ativas.to_sql("operadoras_ativas", conn, index=False, if_exists="replace")

query = """
SELECT 
    RC.Registro_ANS, 
    RC.Razao_Social,
    OA.DESCRICAO,
    (OA.VL_SALDO_INICIAL - OA.VL_SALDO_FINAL) AS VL_DESPESA,
    OA.DATA 
FROM
    Relatorio_cadop as RC
JOIN 
    operadoras_ativas as OA ON RC.Registro_ANS = OA.REG_ANS
WHERE
    OA.DESCRICAO LIKE "%SINISTROS CONHECIDOS OU AVISADOS DE ASSIST%"
ORDER BY VL_DESPESA
LIMIT 10;
"""
resultado = pd.read_sql_query(query, conn)

print("\nPrimeiros 5 registros:")
print(resultado)

conn.execute

conn.close()