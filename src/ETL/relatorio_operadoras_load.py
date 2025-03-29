import sqlite3
import pandas as pd
import glob
import os

relatorio_cadop_path = ("data\\output\\Teste3\\Relatorio\\Relatorio_cadop.csv")
output_dir = ("data\\output\\Teste3\\Periodos")
operadoras_ativas_path = ("data\\output\\Teste3\\Periodos\\Operadoras_ativas_2_ultimos_anos.csv")

os.makedirs(output_dir, exist_ok=True)

def merge_files():
    file_pattern = ("*T*.csv")

    files = glob.glob(os.path.join(output_dir, file_pattern))

    dfs = []
    for file in files:
        df = pd.read_csv(file, encoding="utf-8", sep=";", engine="python")
        dfs.append(df)

    df_consolidated = pd.concat(dfs, ignore_index=True)

    df_consolidated.to_csv(operadoras_ativas_path, index=False, encoding="utf-8-sig", sep=";")
    
    print(df_consolidated)

def load_datas():
    df_relatorio_cadop = pd.read_csv(relatorio_cadop_path, encoding='utf-8-sig', sep=';')
    df_operadoras_ativas = pd.read_csv(operadoras_ativas_path, encoding='utf-8-sig', sep=';')
    return df_relatorio_cadop, df_operadoras_ativas

def create_database(df_relatorio_cadop, df_operadoras_ativas):
    conn = sqlite3.connect(":memory:")
    df_relatorio_cadop.to_sql("Relatorio_cadop", conn, index=False, if_exists="replace")
    df_operadoras_ativas.to_sql("operadoras_ativas", conn, index=False, if_exists="replace")
    return conn

def execute_query(conn):
    
    query = """
    SELECT
        RC.Registro_ANS,
        RC.CNPJ,
        RC.Razao_Social,
        RC.Modalidade,
        RC.Logradouro,
        RC.Numero,
        RC.Bairro,
        RC.Cidade,
        RC.UF,
        RC.CEP,
        RC.Endereco_eletronico AS Email,
        OA.DESCRICAO AS Descricao,
        SUM(OA.VL_SALDO_INICIAL) AS VL_Saldo_Inicial,
        SUM(OA.VL_SALDO_FINAL) AS VL_Saldo_Final,
        OA.DATA AS Periodo
    FROM 
        Relatorio_cadop as RC
    JOIN 
        operadoras_ativas as OA ON RC.Registro_ANS = OA.REG_ANS
    GROUP BY
        OA.DESCRICAO
    """
    return pd.read_sql_query(query, conn)

def save_query_result(query_result):

    output_file = output_dir + "\\Ralatorio_normalizado.csv"
    query_result.to_csv(output_file, index=False, encoding="utf-8-sig", sep=";")