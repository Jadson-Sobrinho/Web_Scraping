from flask import Blueprint, Response, request
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from database.db_connection import get_db_connection

bp = Blueprint('quarter', __name__)

@bp.route("/api/data/quarter", methods=["GET"])
def get_datas():
    conn = get_db_connection()
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    offset = (page - 1) * page_size

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
