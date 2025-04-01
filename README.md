# Ferramentas e Bibliotecas utilizadas
1. Bibliotecas para Manipulação de Arquivos e Diretórios
    os → Criar diretórios e manipular caminhos de arquivos.

    pathlib.Path → Gerenciar caminhos de arquivos e diretórios de forma mais organizada.

    glob → Buscar arquivos em diretórios com padrões específicos.

    zipfile → Compactar e descompactar arquivos ZIP.

2. Web Scraping e Requisições HTTP
    requests → Fazer requisições HTTP para baixar arquivos e acessar páginas web.

    BeautifulSoup (do bs4) → Fazer parsing de HTML para extrair links e informações das páginas.

3. Manipulação de Dados
    pandas → Processar, manipular e analisar dados estruturados (arquivos CSV, tabelas extraídas de PDFs).

    pdfplumber → Extrair tabelas e informações de arquivos PDF.

4. Banco de Dados
    sqlite3 (via database.db_connection) → Gerenciar e armazenar dados em um banco SQLite.

    pandas.to_sql() → Inserir dados diretamente do Pandas para o banco de dados.

5. Framework Web para API
    Flask → Criar um servidor web e expor APIs.

    flask.Blueprint → Modularizar rotas da API.

    flask.Response → Retornar respostas JSON da API.

    flask.request → Capturar parâmetros de requisição.

6. Outros
    sys → Modificar sys.path para importar módulos de diretórios externos.

    json → Manipular e retornar dados em formato JSON.


## Fluxo
 1. Web-Scraping:
    - Acessar o site governamental; 
    - Procurar pelos Anexos I e II;
    - Fazer o download; 
    - Salvar em um diretorio;
    - Compactar em um arquivo .zip. 

 2. Transformação de dados:
    - Extrair so dados do Anexo I;
    - Salvar os dados em um arquivo .cvs;
    - Substitui as abreviações OD e AMB pela nomeclatura completa;
    - Compacta o arquivo em .zip.

 3. Banco de dados:
    - Acessar o site governamental das demonstrações contabéis;
    - Procurar pelos arquivos dos dois ultimos anos;
    - Baixa os arquivos .zip;
    - Descompacta os arquivo;
    - Mescla todos os arquivos trimestrais em um único arquivo;
    - Acessar o site governamental das operadoras de plano de saúde ativas;
    - Baixa o arquivo de operadoras de plano de saúde ativas;
    - Mescla o arquivo de demonstrações contabéis com o arquivi de operadoras de plano de sáude ativas pelo registro ANS;
    - Carrega os dados do novo arquivo mesclado em um banco de dados com SQLite.
 
 4. API:
    - Realiza uma requisição HTTP com: 10 operadoras com maiores despesas em "EVENTOS/ SINISTROS CONHECIDOS OU 
      AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre;
    - Realia uma requisição com: 10 operadoras com maiores despesas nessa categoria no último ano;
    - Realiza uma requisição pela razão social ou CNPJ ou data ou Resgitro ANS.

## Estrutura das pastas:
```
WEB_SCRAPING/
│── backend/
│   ├── api/
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── lastyear.py
│   │   │   │   ├── operadoras.py
│   │   │   │   ├── quarter.py
│   │   │   ├── app.py
│   │   │   ├── database/
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data.db
│   │   │   │   ├── db_connection.py
│   │   │   ├── datasets/
│   │   │   │   ├── input/
|   |   |   |   |         |── Teste1/
|   |   |   |   |             |── Anexo I
|   |   |   |   |             |── Anexo II
|   |   |   |   |         |── Teste3/
|   |   |   |   |         |         |── Periodos/
|   |   |   |   |         |         |── 1T2023.zip
|   |   |   |   |         |         |── 2T2023.zip
|   |   |   |   |         |         |── 3T2023.zip
|   |   |   |   |         |         |── 4T2023.zip
|   |   |   |   |         |         |── 1T2024.zip
|   |   |   |   |         |         |── 2T2024.zip
|   |   |   |   |         |         |── 3T2024.zip
|   |   |   |   |         |         |── 4T2024.zip
│   │   │   │   ├── output/
|   |   |   |   |         |── Teste1/
|   |   |   |   |             |── Anexo I.zip
|   |   |   |   |         |── Teste3/
|   |   |   |   |         |         |── Periodos/
|   |   |   |   |         |             |── 1T2023.csv
|   |   |   |   |         |             |── 2T2023.csv
|   |   |   |   |         |             |── 3T2023.csv
|   |   |   |   |         |             |── 4T2023.csv
|   |   |   |   |         |             |── 1T2024.csv
|   |   |   |   |         |             |── 2T2024.csv
|   |   |   |   |         |             |── 3T2024.csv
|   |   |   |   |         |             |── 4T2024.csv
|   |   |   |   |         |         |── Relatorio/
|   |   |   |   |         |             |── Relatorio_cadop.csv
|   |   |   |   |         |         |── Relatorio_normalizado.csv
│   ├── download/
│   │   ├── __init__.py
│   │   ├── demonstracoes_contabeis.py
│   │   ├── operadoras_ativas.py
│   │   ├── rol_procedimentos.py
│   ├── ETL/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── relatorio_normalizado_database_load.py
│   │   ├── relatorio_operadoras_csv_load.py
│   │   ├── rol_procedimentos_transform.py
├── config/
|   |── .env
├── frontend/
├──.gitignore
├── README.md
├── Requirements.txt
├── TesteTecnico.postman_collection.json

```

## Fluxo de execução
  1. Vá na pasta download/rol_procedimentos.py e execute;
  2. Vá na pasta ETL/rol_procedimentos_transform.py e execute;
  3. Vá na pasta download/demonstracoes_contabeis.py e execute;
  4. Vá na pasta download/operadoras_ativas.py e execute;
  5. Vá na pasta ETL/relatorio_operadoras_csv_load.py e execute;
  6. Vá na pasta ETL/relatorio_normalizado_database_load e execute;
  7. Vá em api/src/app.py e execute;
  8. Vá em api/src/routes e execute as rotas que deseja ou importar as coleção com as requisições do postman.

## Documentação dos códigos
  1. download/rol_procedimentos.py:
      ```
      requests.get(url): Acessa a página do governo e obtém seu conteúdo HTML.
  
      BeautifulSoup(response.text, 'html.parser'): Analisa o HTML da página.
  
      soup.find_all('a', href=True): Busca todos os links da página.
  
      pdf_link.startswith('http'): Garante que o link seja absoluto.
  
      requests.get(pdf_link): Faz o download do PDF.
  
      zipfile.ZipFile(zip, "w"): Compacta todos os arquivos baixados em um ZIP.
      ```

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
  - Criar validação das entradas que vem pela requisição;
  - Trocar o recebimento de requisições da URL pelo JSON;
  - Não mesclar os dados das operadoras de plano de saúde ativa e demonstrações contabeis, colocar cada arquivo como uma tabela para otimizar a consulta de dados;
  - Utilizar Spark para grande quantidade de dados;
  - Refatorar as query's;
  - Adicionar Indeces nos campos mais utilizados;
  - Pesquisar por alguma ORM;
  - Integrar ao front-end com framework vue.js
