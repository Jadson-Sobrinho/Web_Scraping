import os
import glob
import pandas as pd


relatorio_cadop_path = "backend\\datasets\\output\\Teste3\\Relatorio\\Relatorio_cadop.csv"
output_dir = "backend\\datasets\\output\\Teste3\\Periodos"
base_path = "backend\\datasets\\output\\Teste3"
operadoras_ativas_path = os.path.join(output_dir, "Operadoras_ativas_2_ultimos_anos.csv")
relatorio_normalizado_path = os.path.join(base_path, "Relatorio_normalizado.csv")

os.makedirs(output_dir, exist_ok=True)

def merge_files():
    file_pattern = "*T*.csv"
    files = glob.glob(os.path.join(output_dir, file_pattern))
    
    if not files:
        raise FileNotFoundError("Nenhum arquivo encontrado com o padrão especificado.")
    
    dfs =[]
    for file in files:
        chunk = pd.read_csv(file, encoding="utf-8", sep=";", engine="c")

        try:
            chunk["DATA"] = pd.to_datetime(chunk["DATA"], format="%Y-%m-%d").dt.strftime("%Y-%m-%d")
        except ValueError:
            chunk["DATA"] = pd.to_datetime(chunk["DATA"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
        dfs.append(chunk)

    
    #dfs = [pd.read_csv(file, encoding="utf-8", sep=";", engine="c") for file in files]
    df_consolidated = pd.concat(dfs, ignore_index=True)
    df_consolidated.to_csv(operadoras_ativas_path, index=False, encoding="utf-8-sig", sep=";")
    return df_consolidated

def load_datas():
    df_relatorio_cadop = pd.read_csv(relatorio_cadop_path, encoding='utf-8-sig', sep=';')
    df_operadoras_ativas = pd.read_csv(operadoras_ativas_path, encoding='utf-8-sig', sep=';')
    return df_relatorio_cadop, df_operadoras_ativas

def merge_datasets(df_relatorio_cadop, df_operadoras_ativas):
    #Convete os dados das colunas em numerico (estavam sendo interpretadas como string, por isso não estava fazendo o calculo)
    df_operadoras_ativas["VL_SALDO_INICIAL"] = df_operadoras_ativas["VL_SALDO_INICIAL"].str.replace(".", "").str.replace(",", ".").astype(float)
    df_operadoras_ativas["VL_SALDO_FINAL"] = df_operadoras_ativas["VL_SALDO_FINAL"].str.replace(".", "").str.replace(",", ".").astype(float)
    #print(df_operadoras_ativas["DATA"].sample(10).unique())

    save_query_result
    df_merged = pd.merge(
        df_relatorio_cadop,
        df_operadoras_ativas,
        left_on="Registro_ANS",
        right_on="REG_ANS",
        how="right"
    )
    return df_merged

def save_query_result(df, output_file=relatorio_normalizado_path):
    df.to_csv(output_file, index=False, encoding="utf-8-sig", sep=";")

merge_files()
df_relatorio_cadop, df_operadoras_ativas = load_datas()
df_final = merge_datasets(df_relatorio_cadop, df_operadoras_ativas)
#print(df_final)
save_query_result(df_final)