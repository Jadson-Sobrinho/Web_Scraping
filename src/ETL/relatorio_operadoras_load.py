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
    
    #print(df_consolidated)

merge_files()