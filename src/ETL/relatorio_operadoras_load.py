import os
import glob
import pandas as pd


relatorio_cadop_path = "data/output/Teste3/Relatorio/Relatorio_cadop.csv"
output_dir = "data/output/Teste3/Periodos"
base_path = "data/output/Teste3"
operadoras_ativas_path = os.path.join(output_dir, "Operadoras_ativas_2_ultimos_anos.csv")
relatorio_normalizado_path = os.path.join(base_path, "Relatorio_normalizado.csv")

os.makedirs(output_dir, exist_ok=True)

def merge_files():
    file_pattern = "*T*.csv"
    files = glob.glob(os.path.join(output_dir, file_pattern))
    
    if not files:
        raise FileNotFoundError("Nenhum arquivo encontrado com o padrão especificado.")
    
    dfs = [pd.read_csv(file, encoding="utf-8", sep=";", engine="c") for file in files]
    df_consolidated = pd.concat(dfs, ignore_index=True)
    df_consolidated.to_csv(operadoras_ativas_path, index=False, encoding="utf-8-sig", sep=";")
    return df_consolidated

def load_datas():
    df_relatorio_cadop = pd.read_csv(relatorio_cadop_path, encoding='utf-8-sig', sep=';')
    df_operadoras_ativas = pd.read_csv(operadoras_ativas_path, encoding='utf-8-sig', sep=';')
    return df_relatorio_cadop, df_operadoras_ativas

def merge_datasets(df_relatorio_cadop, df_operadoras_ativas):
    #Convete os dados das colunas em numerico (estavam sendo interpretadas como string, por isso não estava fazendo o calculo)
    df_operadoras_ativas["VL_SALDO_INICIAL"] = pd.to_numeric(df_operadoras_ativas["VL_SALDO_INICIAL"], errors="coerce")
    df_operadoras_ativas["VL_SALDO_FINAL"] = pd.to_numeric(df_operadoras_ativas["VL_SALDO_FINAL"], errors="coerce")
    
    df_merged = pd.merge(
        df_relatorio_cadop,
        df_operadoras_ativas,
        left_on="Registro_ANS",
        right_on="REG_ANS",
        how="inner"
    )
    df_merged["Despesas"] = df_merged["VL_SALDO_FINAL"] - df_merged["VL_SALDO_INICIAL"]
    return df_merged

def save_query_result(df, output_file=relatorio_normalizado_path):
    df.to_csv(output_file, index=False, encoding="utf-8-sig", sep=";")