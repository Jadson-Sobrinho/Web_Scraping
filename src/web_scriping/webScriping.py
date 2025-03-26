import requests
from bs4 import BeautifulSoup
import os
import zipfile



url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

#TO-DO: Criar diretorio para os anexos caso não exista 

#TO_DO: Colocar as variaveis de diretorios no env

input_dir = 'C:\\Users\\c31f4\\OneDrive\\Desktop\\PROJETOS\\Web_Scraping\\data\\input'
response = requests.get(url)
pdf_files = []


if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = soup.find_all('a', href=True)
    pdf_links = []
    
    for link in links:
        href = link['href']
        if href.endswith('.pdf') and 'Anexo' in href:
            pdf_links.append(href)
    

    for pdf_link in pdf_links:
        if not pdf_link.startswith('http'):
            pdf_link = f"https://www.gov.br{pdf_link}"
        
        pdf_response = requests.get(pdf_link)
        

        if pdf_response.status_code == 200: 
            file_name = pdf_link.split('/')[-1]
            pdf_path = os.path.join(input_dir, file_name)

            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)

            pdf_files.append(pdf_path)
            print("ok")
            
        else:
            print("erro")
else:
    print("Erro ao acessar o site")

zip = input_dir + ".zip"
with zipfile.ZipFile(zip, "w") as zipped:
    for pdf in pdf_files:
        zipped.write(pdf, os.path.basename(pdf))

print("zipped")


