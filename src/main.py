import ETL

def main():
    
    df_relatorio_cadop, df_operadoras_ativas = ETL.load_datas()
    query_result = ETL.process_data(df_relatorio_cadop, df_operadoras_ativas)
    ETL.save_query_result(query_result)

    ETL.normalize_df()
    ETL.zip_file()

if __name__ == "__main__":
    main()