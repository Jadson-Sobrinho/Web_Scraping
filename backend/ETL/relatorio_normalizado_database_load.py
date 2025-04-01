import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#print("sys.path: ", sys.path)
from database.db_connection import get_db_connection, db_path


csv_path = "backend\\datasets\\output\\Teste3\\Relatorio_normalizado.csv"


def import_csv_into_db(csv_path, db_path, chunk_size=2000):
    
    conn = get_db_connection()
    

    for chunk in pd.read_csv(csv_path, sep=";", encoding="utf-8-sig", chunksize=chunk_size):

        #chunk["VL_SALDO_INICIAL"] = pd.to_numeric(chunk["VL_SALDO_INICIAL"], errors="coerce")
        #chunk["VL_SALDO_FINAL"] = pd.to_numeric(chunk["VL_SALDO_FINAL"], errors="coerce")


        chunk.to_sql("empresa", conn, if_exists="append", index=False)

    conn.close()
    print("Dados importados")


import_csv_into_db(csv_path, db_path)