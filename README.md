# Documentação do Projeto

## Ferramentas e Bibliotecas Utilizadas

### 1. Manipulação de Arquivos e Diretórios
- **`os`**: Criar diretórios e manipular caminhos
- **`pathlib.Path`**: Gerenciar caminhos de forma organizada
- **`glob`**: Buscar arquivos com padrões específicos
- **`zipfile`**: Compactar/descompactar arquivos ZIP

### 2. Web Scraping e HTTP
- **`requests`**: Requisições HTTP
- **`BeautifulSoup (bs4)`**: Parsing de HTML

### 3. Manipulação de Dados
- **`pandas`**: Processamento de dados estruturados
- **`pdfplumber`**: Extração de dados de PDFs

### 4. Banco de Dados
- **`sqlite3`**: Banco de dados SQLite
- **`pandas.to_sql()`**: Inserção de dados no banco

### 5. Framework Web (API)
- **`Flask`**: Servidor web e APIs
- **`flask.Blueprint`**: Modularização de rotas
- **`flask.Response`**: Respostas JSON
- **`flask.request`**: Captura de parâmetros

### 6. Outros
- **`sys`**: Manipulação de sys.path
- **`json`**: Manipulação de JSON

---

## 🔄 Fluxo Principal

### 1. Web-Scraping
- Acessar site governamental
- Localizar e baixar Anexos I e II
- Salvar em diretório específico
- Compactar em .zip

### 2. Transformação de Dados
- Extrair dados do Anexo I
- Salvar em CSV
- Substituir abreviações (OD → Odontológico, AMB → Ambulatorial)
- Compactar em .zip

### 3. Banco de Dados
- Baixar arquivos dos últimos 2 anos
- Descompactar e mesclar trimestres
- Baixar dados de operadoras ativas
- Mesclar datasets pelo Registro ANS
- Carregar no SQLite

### 4. API
- Endpoints:
  - Top 10 operadoras com maiores despesas (último trimestre)
  - Top 10 operadoras com maiores despesas (último ano)
  - Busca por razão social/CNPJ/data/Registro ANS

---

## Estrutura de Pastas

```plaintext
WEB_SCRAPING/
│── backend/
│   ├── api/
│   │   ├── src/
│   │   │   ├── routes/              # Rotas da API
│   │   │   ├── app.py               # Aplicação Flask
│   │   │   ├── database/            # Configurações do banco
│   │   │   ├── datasets/            # Arquivos de entrada/saída
│   ├── download/                    # Scripts de download
│   ├── ETL/                         # Scripts de transformação
├── config/                          # Configurações
├── frontend/                        # Frontend (futura implementação)
├── .gitignore
├── README.md
├── Requirements.txt
├── TesteTecnico.postman_collection.json
```
## Documentação dos códigos
  1. download/rol_procedimentos.py:

    requests.get(url): Acessa a página do governo e obtém seu conteúdo HTML.

    BeautifulSoup(response.text, 'html.parser'): Analisa o HTML da página.

    soup.find_all('a', href=True): Busca todos os links da página.

    pdf_link.startswith('http'): Garante que o link seja absoluto.

    requests.get(pdf_link): Faz o download do PDF.

    zipfile.ZipFile(zip, "w"): Compacta todos os arquivos baixados em um ZIP.
    

  2. ETL/rol_procedimentos_transform.py:
      ```
      extract_data_into_dt(): Lê todas as páginas do PDF e extrai as tabelas.

      normalize_df(): Junta os dados extraídos, substitui valores e os salva em um CSV.

      zip_file(): Compacta o arquivo CSV gerado.
      


  3. download/demonstracoes_contabeis.py: 
      ```
      requests.get(year_url): Obtém o conteúdo da página HTML do diretório de arquivos.

      BeautifulSoup(response.text, 'html.parser'): Analisa o HTML da página.

      for link in soup.find_all("a", href=True): Percorre todos os links disponíveis na página.

      file_name.endswith(".zip"): Filtra apenas os arquivos ZIP.

      requests.get(zip_url, stream=True): Faz o download do arquivo ZIP.

      zipfile.ZipFile(zip_path, 'r').extractall(output_dir): Extrai os arquivos ZIP para o diretório de saída.
      ```

  4. download/operadoras_ativas.py:
      ```
      requests.get(url, timeout=10): Faz uma requisição HTTP para acessar a página da ANS.

      BeautifulSoup(response.text, 'html.parser'): Analisa o código HTML da página.

      soup.find_all("a", href=True): Busca todos os links na página.

      file_name.endswith(".csv"): Filtra apenas os arquivos com extensão CSV.

      requests.get(file_url, stream=True): Faz o download do arquivo CSV.

      os.makedirs(output_dir, exist_ok=True): Garante que o diretório de saída exista antes de salvar os arquivos.
      ```

  5. ETL/relatorio_operadoras_csv_load.py:
      ```
      merge_files(): Encontra e combina arquivos CSV de operadoras ativas.

      load_datas(): Carrega os dados dos arquivos CSV principais.

      merge_datasets(): Faz a junção dos dados normalizando valores numéricos.

      save_query_result(): Exporta o dataframe final para um CSV.
      ```

  6. ETL/relatorio_normalizado_database_load:
      ```
      sys.path.append(...): Adiciona o caminho do banco para importação.

      get_db_connection(): Estabelece conexão com o banco.

      pd.read_csv(..., chunksize=2000): Lê o CSV em blocos de 2000 linhas.

      to_sql(): Insere os dados na tabela empresa.

      conn.close(): Fecha a conexão após a importação.
      ```

  7. api/src/app.py:
      ```
      register_blueprint() para modularizar as rotas.

      ```

## TODO's
  Criar validação das entradas que vem pela requisição;
  Trocar o recebimento de requisições da URL pelo JSON;
  Não mesclar os dados das operadoras de plano de saúde ativa e demonstrações contabeis, colocar cada arquivo como uma tabela para otimizar a consulta de dados;
  Utilizar Spark para grande quantidade de dados;
  Refatorar as query's;
  Pesquisar por alguma ORM;
  Integrar ao front-end com framework vue.js
