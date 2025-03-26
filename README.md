## Web Scraping e Compactação de PDFs

Este código faz web scraping para baixar arquivos PDF de um site governamental e depois os compacta em um arquivo ZIP.

---

### Web Scraping:
- Acessa a URL da ANS (Agência Nacional de Saúde Suplementar);
- Busca todos os links;
- Verifica dentro da lista de links os arquivos PDF com "Anexo" no nome;
- Baixa esses arquivos para uma pasta local.

### Manipulação de Arquivos:
- Armazenas os PDFs no diretorio (`input_dir`)
- Compacta todos os PDFs baixados em um único arquivo ZIP com o mesmo nome da pasta + extensão `.zip`

---

## Fluxo Detalhado
1. Importa bibliotecas necessárias (`requests`, `BeautifulSoup`, `os`, `zipfile`)
2. Define a URL alvo do scraping
3. Define o diretório onde os arquivos serão salvos (`input_dir`)
4. Faz a requisição HTTP para a URL
5. Se a requisição for bem-sucedida (status 200):
   - Analisa o HTML com `BeautifulSoup`
   - Encontra todos os links que terminam com `.pdf` e contêm "Anexo" na URL
   - Para cada link encontrado:
     - Completa a URL se for relativa (adiciona o domínio `gov.br`)
     - Faz o download do PDF
     - Salva no diretório especificado
6. Cria um arquivo ZIP com todos os PDFs baixados
7. Imprime mensagens de status durante o processo

---

## TO-DOs
- Criar o diretório para os anexos caso não exista
- Colocar as variáveis de diretórios no ambiente
