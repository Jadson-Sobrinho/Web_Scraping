import pdfplumber
import pandas as pd
import os
import zipfile


#TO_DO: Importar o caminho do pacote de werb_scraping ou verficar se tem no diretorio "input"

#TO_DO: Colocar o diretorio no env

pdf_path = "C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\input\\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
output_dir = "C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\output"
csv_path = os.path.join(output_dir, "Rol_processedimentos_eventos.csv")


def extract_data_into_dt():
    completed_table = []
    
    with pdfplumber.open(pdf_path) as pdf:
        
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                df = pd.DataFrame(table)
                completed_table.append(df)

    return completed_table

extract_data = extract_data_into_dt()

def normalize_df():
    
    if extract_data:
        final_df = pd.concat(extract_data, ignore_index=True)
        #print(final_df)

        final_df.replace({"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}, inplace=True)

        final_df.to_csv(csv_path, index=False, encoding="utf-8-sig", sep=";")
        #print(completed_table)

    else:
        print("Nenhuma tabela encontrada")

def zip_file():
    zip_name = os.path.join(output_dir, f"Teste_Jadson_Sobrinho.zip")

    with zipfile.ZipFile(zip_name, "w") as zipped:
        zipped.write(csv_path, os.path.basename(csv_path))

    print("zipped")

normalize_df()
zip_file()