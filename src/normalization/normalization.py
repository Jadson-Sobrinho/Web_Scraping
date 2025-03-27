import pdfplumber
import pandas as pd
import os


#TO_DO: Importar o caminho do pacote de werb_scraping ou verficar se tem no diretorio "input"

#TO_DO: Colocar o diretorio no env

pdf_path = "C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\input\\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
output_dir = "C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\output"
csv_path = os.path.join(output_dir, "final_output.csv")
completed_table = []

with pdfplumber.open(pdf_path) as pdf:
    
    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            df = pd.DataFrame(table)
            completed_table.append(df)

if completed_table:
    final_df = pd.concat(completed_table, ignore_index=True)
    #print(final_df)
    final_df.to_csv(csv_path, index=False, encoding="utf-8-sig", sep=";")
    #print(completed_table)

else:
    print("Nenhuma tabela encontrada")

