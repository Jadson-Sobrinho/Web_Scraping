from flask import Flask, Response, request, jsonify
import csv
import json
import os
import sqlite3
from collections import OrderedDict #Deixa na ordem ao converter para JSON
import pandas as pd


#TO-DO: Normalizar as datas em um formato só


app = Flask(__name__)


db_path = "dados.db"
csv_path = "C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\output\\Teste3\\Relatorio_normalizado.csv"

def get_db_connection():
    """Cria e retorna uma conexão com o banco SQLite."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelo nome
    return conn


def import_csv(csv_path, db_path, chunk_size=2000):
    
    conn = sqlite3.connect(db_path)

    for chunk in pd.read_csv(csv_path, sep=";", encoding="utf-8-sig", chunksize=chunk_size):

        #chunk["VL_SALDO_INICIAL"] = pd.to_numeric(chunk["VL_SALDO_INICIAL"], errors="coerce")
        #chunk["VL_SALDO_FINAL"] = pd.to_numeric(chunk["VL_SALDO_FINAL"], errors="coerce")


        chunk.to_sql("empresa", conn, if_exists="append", index=False)

    conn.close()
    print("Dados importados")


import_csv(csv_path, db_path)

@app.route("/api/data", methods=["GET"])
def obter_dados():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    offset = (page - 1) * page_size

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT 
                        Registro_ANS, 
                        CNPJ, 
                        Razao_Social, 
                        DESCRICAO, 
                        SUM(VL_SALDO_INICIAL) AS VL_SALDO_INICIAL, 
                        SUM(VL_SALDO_FINAL) AS VL_SALDO_FINAL,
                        SUM(VL_SALDO_INICIAL - VL_SALDO_FINAL) AS Despesa,
                        DATA
                    FROM empresa
                    WHERE 
                        DESCRICAO LIKE "%SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%" 
                        AND DATA = "2024-10-01"
                    GROUP BY 
                        Registro_ANS,
                        CNPJ,
                        Razao_Social,  
                        DESCRICAO,
                        DATA
                    HAVING SUM(VL_SALDO_INICIAL - VL_SALDO_FINAL) > 1
                    ORDER BY Despesa DESC 
                    LIMIT 10;
                   """)
    lines = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in lines ]
    json_output = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False)
    return Response(json_output, content_type="application/json")

if __name__ == '__main__':
    app.run(debug=True)


