import pandas as pd
import sqlite3
import csv  # Per gestire il salvataggio corretto del CSV
import numpy as np

def check_table_exists(conn, table_name):
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    result = conn.execute(query).fetchone()
    if result is None:
        print(f"ERRORE: La tabella '{table_name}' non esiste nel database.")

def process_csv_same_lang(df_csv, conn, db_table, db_column, search_value):
    check_table_exists(conn, db_table)

    query = f"SELECT {db_column} FROM '{db_table}'"
    df_db = pd.read_sql(query, conn)

    mask = df_csv.iloc[:, 0] == search_value
    num_replacements = mask.sum()

    if num_replacements == 0:
        print(f"ATTENZIONE: Nessuna riga trovata con '{search_value}' nel CSV.")
        return

    if num_replacements != len(df_db):
        print(f"ATTENZIONE: il numero di righe differisce per '{search_value}' / '{db_table}': CSV={num_replacements}, DB={len(df_db)}. Verranno usati i primi {min(num_replacements, len(df_db))} valori.")

    limite = min(num_replacements, len(df_db))
    values_from_db = df_db[db_column].values[:limite]

    if db_column == "measurment_unit":
        value_to_copy = np.array([f"[{val}]" for val in values_from_db])
    else:
        value_to_copy = values_from_db

    righe_csv = df_csv.loc[mask].head(limite).index
    df_csv.loc[righe_csv, df_csv.columns[2]] = value_to_copy

    for i in range(3, 6):
        if i < len(df_csv.columns):
            df_csv.loc[righe_csv, df_csv.columns[i]] = df_csv.loc[righe_csv, df_csv.columns[2]]

def process_csv_events(df_csv, conn, db_table, db_column_eng, db_column_ita, search_value):
    check_table_exists(conn, db_table)

    query = f"SELECT {db_column_eng}, {db_column_ita} FROM '{db_table}'"
    df_db = pd.read_sql(query, conn)

    mask = df_csv.iloc[:, 0] == search_value
    num_replacements = mask.sum()

    if num_replacements == 0:
        print(f"ATTENZIONE: Nessuna riga trovata con '{search_value}' nel CSV.")
        return

    if num_replacements != len(df_db):
        print(f"ATTENZIONE: il numero di righe differisce per '{search_value}' / '{db_table}': CSV={num_replacements}, DB={len(df_db)}. Verranno usati i primi {min(num_replacements, len(df_db))} valori.")

    limite = min(num_replacements, len(df_db))
    righe_csv = df_csv.loc[mask].head(limite).index

    df_csv.loc[righe_csv, "Default"] = df_db[db_column_eng].values[:limite]
    df_csv.loc[righe_csv, "EN"] = df_db[db_column_eng].values[:limite]
    df_csv.loc[righe_csv, "FR"] = df_db[db_column_eng].values[:limite]
    df_csv.loc[righe_csv, "IT"] = df_db[db_column_ita].values[:limite]

    print(f"SUCCESSO: Aggiornate {limite} righe con dati da '{db_table}'.")
