from flask import Flask, Response, request, jsonify
import csv
import json
import os

app = Flask(__name__)

path = "C:/Users/c31f4/OneDrive/Desktop/PROJETOS/Web_Scraping/data/input/Relatorio_cadop.csv"

@app.route("/api/data", methods=["GET"])
def get_datas():
    datas = []
    with open(path, "r", encoding="utf-8") as csv_file:
        read_csv = csv.DictReader(csv_file,  delimiter=';')
        for line in read_csv:
            processed_line = {k: (v if v is not None else "") for k, v in line.items()}
            datas.append(processed_line)
    return Response(
        json.dumps(datas, ensure_ascii=False, indent=4),
        mimetype="application/json; charset=utf-8"
    )

@app.route("/api/data/filter", methods=["GET"])
def filter_datas():
    try:
      
        cnpj = request.args.get("CNPJ")
        if not cnpj:
            return jsonify({"error": "CNPJ é obrigatório"}), 400
        
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        if len(cnpj_clean) != 14:
            return jsonify({"error": "CNPJ deve conter 14 dígitos"}), 400

        filtrate_data = []
        
        # Verifica se arquivo existe
        if not os.path.exists(path):
            return jsonify({"error": "Arquivo CSV não encontrado"}), 404

        with open(path, "r", encoding="utf-8") as csv_file:
            read_csv = csv.DictReader(csv_file, delimiter=";")
            
            for line in read_csv:
                # Processa linha e limpa CNPJ do arquivo
                processed_line = {k: (v.strip() if v else "") for k, v in line.items()}
                file_cnpj = processed_line.get("CNPJ", "")
                file_cnpj_clean = ''.join(filter(str.isdigit, file_cnpj))
                
                # Compara CNPJs limpos (sem formatação)
                if file_cnpj_clean == cnpj_clean:
                    filtrate_data.append(processed_line)

        if not filtrate_data:
            return jsonify({"message": "Nenhum CNPJ encontrado"}), 404

        return Response(
            json.dumps(filtrate_data, ensure_ascii=False, indent=4),
            mimetype="application/json; charset=utf-8"
        )

    except Exception as e:
        return jsonify({"error": f"Erro ao processar a requisição: {str(e)}"}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True) 