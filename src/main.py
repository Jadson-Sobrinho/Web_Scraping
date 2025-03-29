import ETL

def main():
    
    df_relatorio_cadop, df_operadoras_ativas = ETL.load_datas()
    conn = ETL.create_database(df_relatorio_cadop, df_operadoras_ativas)
    query_result = ETL.execute_query(conn)
    conn.close()
    ETL.save_query_result(query_result)

    ETL.normalize_df()
    ETL.zip_file()

if __name__ == "__main__":
    main()