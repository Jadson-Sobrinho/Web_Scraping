from flask import Blueprint, Response, request
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from database.db_connection import get_db_connection

bp = Blueprint('operadoras', __name__)

@bp.route("/api/data/operadoras", methods=["GET"])
def get_datas():
    conn = get_db_connection()
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    offset = (page - 1) * page_size

    Razao_Social = request.args.get("Razao_Social")
    CNPJ = request.args.get("CNPJ")
    Registro_ANS = request.args.get("Registro_ANS")
    DATA = request.args.get("DATA")
    search_Razao_Social_pattern = f"%{Razao_Social}%"

    cursor = conn.cursor()

    

    # TO-DO: Ajustar para fazer uma consulta dinamicamente
    # TO-DO: Adicionar filtro de periodo de inicio e fim
    
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
                        (Razao_Social LIKE ? OR ? IS NULL)
                        AND (CNPJ = ? OR ? IS NULL)
                        AND (Registro_ANS = ? OR ? IS NULL)
                        AND (DATA = ? OR ? IS NULL)
                   GROUP BY 
                        Registro_ANS, 
                        CNPJ, 
                        Razao_Social,  
                        DESCRICAO, 
                        DATA
                    ORDER BY 
                        DATA DESC
                    LIMIT 100;
                   """, (search_Razao_Social_pattern,
                         search_Razao_Social_pattern,
                         CNPJ,
                         CNPJ,  
                         Registro_ANS,
                         Registro_ANS, 
                         DATA,
                         DATA ))

    lines = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in lines ]
    json_output = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=False)
    return Response(json_output, content_type="application/json")
