from flask import Flask, Response, request, jsonify
import csv
import json
import os
import sqlite3
from collections import OrderedDict #Deixa na ordem ao converter para JSON

#TO-DO: Verificar pq os dados de valores estão retornando nulos


app = Flask(__name__)


DATABASE = "dados.db"
csv_path = "C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\output\\Teste3\\Relatorio_normalizado.csv"

def get_db_connection():
    """Cria e retorna uma conexão com o banco SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelo nome
    return conn

def create_table():
    """Cria a tabela 'empresa' caso ela não exista."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS empresa (
            registro_ans TEXT PRIMARY KEY,
            cnpj TEXT,
            razao_social TEXT,
            modalidade TEXT,
            logradouro TEXT,
            numero TEXT,
            bairro TEXT,
            cidade TEXT,
            uf TEXT,
            cep TEXT,
            endereco_eletronico TEXT,
            descricao TEXT,
            vl_saldo_inicial TEXT,
            vl_saldo_final TEXT,
            despesas TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def import_csv():
    """Importa os dados do arquivo CSV para a tabela 'empresa'."""
    if not os.path.exists(csv_path):
        print("Arquivo não encontrado")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    with open(csv_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        for line in reader:

            
            registro_ans = line.get("Registro_ANS", "").strip()
            cnpj = line.get("CNPJ", "").strip()
            razao_social = line.get("Razao_Social", "").strip()
            modalidade = line.get("Modalidade", "").strip()
            logradouro = line.get("Logradouro", "").strip()
            numero = line.get("Numero", "").strip()
            bairro = line.get("Bairro", "").strip()
            cidade = line.get("Cidade", "").strip()
            uf = line.get("UF", "").strip()
            cep = line.get("CEP", "").strip()
            endereco_eletronico = line.get("Endereco_eletronico", "").strip()
            descricao = line.get("DESCRICAO", "").strip()
            vl_saldo_inicial = line.get("VL_SALDO_INICIAL", "").strip()
            vl_saldo_final = line.get("VL_SALDO_FINAL", "").strip()
            despesas = line.get("Despesas", "").strip()


            try:
                vl_saldo_inicial = float(vl_saldo_inicial) if vl_saldo_inicial else None
            except ValueError:
                vl_saldo_inicial = None
            try:
                vl_saldo_final = float(vl_saldo_final) if vl_saldo_final else None
            except ValueError:
                vl_saldo_final = None
            try:
                despesas = float(despesas) if despesas else None
            except ValueError:
                despesas = None

            cursor.execute(
                """
                INSERT OR IGNORE INTO empresa (
                    registro_ans, cnpj, razao_social, modalidade, logradouro, numero,
                    bairro, cidade, uf, cep, endereco_eletronico, descricao, vl_saldo_inicial, vl_saldo_final, despesas
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    registro_ans,
                    cnpj,
                    razao_social,
                    modalidade,
                    logradouro,
                    numero,
                    bairro,
                    cidade,
                    uf,
                    cep,
                    endereco_eletronico,
                    descricao,
                    vl_saldo_inicial,
                    vl_saldo_final,
                    despesas
                )
            )
    conn.commit()
    conn.close()
    print("Dados importados")


create_table()
import_csv()

@app.route("/api/data", methods=["GET"])
def obter_dados():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    offset = (page - 1) * page_size

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT registro_ans,
                    cnpj,
                    razao_social,
                    modalidade,
                    logradouro,
                    numero,
                    bairro,
                    cidade,
                    uf,
                    cep,
                    endereco_eletronico,
                    descricao,
                    vl_saldo_inicial,
                    vl_saldo_final,
                    despesas FROM empresa LIMIT ? OFFSET ?
                   """, (page_size, offset))
    lines = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in lines ]
    json_output = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False)
    return Response(json_output, content_type="application/json")

@app.route("/api/data/filter", methods=["GET"])
def filtrar_dados():
    """Filtra e retorna um registro pelo CNPJ."""
    cnpj = request.args.get("CNPJ")
    if not cnpj:
        return jsonify({"erro": "CNPJ é obrigatório"}), 400

    # Remove caracteres não numéricos do CNPJ
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj_limpo) != 14:
        return jsonify({"erro": "CNPJ deve conter 14 dígitos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresa WHERE cnpj = ?", (cnpj_limpo,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"mensagem": "Nenhum registro encontrado para esse CNPJ"}), 404

    result = OrderedDict([
    ("Registro_ANS", row["registro_ans"]),
    ("CNPJ", row["cnpj"]),
    ("Razao_Social", row["razao_social"]),
    ("Modalidade", row["modalidade"]),
    ("Logradouro", row["logradouro"]),
    ("Numero", row["numero"]),
    ("Bairro", row["bairro"]),
    ("Cidade", row["cidade"]),
    ("UF", row["uf"]),
    ("CEP", row["cep"]),
    ("Endereco_eletronico", row["endereco_eletronico"]),
    ("DESCRICAO", row["descricao"]),
    ("VL_SALDO_INICIAL", row["vl_saldo_inicial"]),
    ("VL_SALDO_FINAL", row["vl_saldo_final"]),
    ("Despesas", row["despesas"])
])

    json_output = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False)
    return Response(json_output, content_type="application/json")

if __name__ == '__main__':
    app.run(debug=True)
