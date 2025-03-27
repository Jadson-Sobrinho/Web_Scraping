import pdfplumber
import pandas as pd


#TO_DO: Importar o caminho do pacote de werb_scraping ou verficar se tem no diretorio "input"
pdf_path = "C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\input\\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

with pdfplumber.open(pdf_path) as pdf:
    completed_table = []

    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            df = pd.DataFrame(table)
            completed_table.append(df)

if completed_table:
    final_df = pd.concat(completed_table, ignore_index=True)
    print(final_df)
else:
    print("Nenhuma tabela encontrada")

