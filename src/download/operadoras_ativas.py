import requests
from bs4 import BeautifulSoup
import os


input_dir = os.getenv('INPUT_DIR', 'C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\input')
output_dir = os.getenv('OUTPUT_DIR', 'C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\output')

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)


url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"

try:

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all("a", href=True):
            file_name = link["href"]
            
            if file_name.endswith(".csv"):
                file_url = f"{url}{file_name}" 
                file_path = os.path.join(input_dir, file_name) 

                print(f"Baixando: {file_name}")

                with requests.get(file_url, stream=True) as r:
                    r.raise_for_status() 
                    with open(file_path, 'wb') as csv_path:
                        for chunk in r.iter_content(chunk_size=8192):
                            csv_path.write(chunk)

                print(f"Salvo")
    else:
        print(f"Erro ao acessar o site")

except requests.exceptions.RequestException as e:
    print(f"Erro {e}")

print("Baixado")
