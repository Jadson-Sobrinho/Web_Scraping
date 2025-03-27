import requests
from bs4 import BeautifulSoup
import os
import zipfile


input_dir = os.getenv('INPUT_DIR', 'C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\input')
output_dir = os.getenv('OUTPUT_DIR', 'C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\output')


os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

years = ["2024", "2023"]


for year in years:
    year_url = f"{url}{year}/"
    
    try:

        response = requests.get(year_url, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all("a", href=True):
                file_name = link["href"]
  
                if file_name.endswith(".zip"):
                    zip_url = f"{year_url}{file_name}"
                    zip_path = os.path.join(input_dir, file_name)

                    print(f"Baixando: {file_name}")

                    with requests.get(zip_url, stream=True) as r:
                        r.raise_for_status()
                        with open(zip_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)

                    print(f"Salvo")

        else:
            print(f"Erro: {year_url} HTTP: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Erro {e}")

print("Baixado")

for file in os.listdir(input_dir):
    if file.endswith(".zip"):
        zip_path = os.path.join(input_dir, file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        print("Extraido: {file}")
