import ETL

def main():
    
    df_relatorio_cadop, df_operadoras_ativas = ETL.load_datas()
    df_final = ETL.merge_datasets(df_relatorio_cadop, df_operadoras_ativas)
    #print(df_final)
    ETL.save_query_result(df_final)

if __name__ == "__main__":
    main()