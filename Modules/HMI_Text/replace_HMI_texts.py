import pandas as pd
import sqlite3
import tkinter as tk
import re
from tkinter import filedialog, messagebox
from Modules.HMI_Text.copy_values import process_csv_same_lang, process_csv_events  # emoji-free version

def scegli_file_csv():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Seleziona il file CSV",
        filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
    )

def scegli_file_db():
    return filedialog.askopenfilename(
        title="Seleziona il database SQLite",
        filetypes=[("Database SQLite", "*.sqlite *.db")]
    )

def analizza_caratteri_a_capo(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("🔍 Verifica caratteri a capo nel database:")
    totali = 0

    for tabella in ["PAR_BOOL", "PAR_INT"]:
        print(f"\n🗂️  Tabella {tabella}:")
        for row in cursor.execute(f"SELECT rowid, global_variable FROM {tabella}"):
            rowid, gv = row
            if not isinstance(gv, str):
                continue
            cleaned = gv.replace('\n', '').replace('\r', '')
            if gv != cleaned:
                totali += 1
                print(f" - [row {rowid}] {repr(gv)} → {repr(cleaned)}")

    if totali == 0:
        print("\n✅ Nessun carattere a capo trovato nelle tabelle.")
    else:
        print(f"\n⚠️  Totale righe da correggere: {totali}")

    conn.close()

def replace_text():
    csv_file = scegli_file_csv()
    if not csv_file:
        messagebox.showwarning("Attenzione", "Nessun file CSV selezionato.")
        return

    db_path = scegli_file_db()
    if not db_path:
        messagebox.showwarning("Attenzione", "Nessun database selezionato.")
        return

    # Analizza il database prima di proseguire
    analizza_caratteri_a_capo(db_path)

    # Carica il CSV
    df_csv = pd.read_csv(csv_file, encoding="utf-16", sep="\t", dtype=str)
    conn = sqlite3.connect(db_path)

    process_csv_same_lang(df_csv, conn, "PAR_BOOL",    "description",      "TextParamDescriptionBool")
    process_csv_same_lang(df_csv, conn, "PAR_INT",     "description",      "TextParamDescriptionInt")
    process_csv_same_lang(df_csv, conn, "PAR_INT",     "measurment_unit",  "TextParamUniMeasureInt")
    process_csv_events( df_csv, conn, "ALARMS",         "eng", "ita",       "TextAlarm")
    process_csv_events( df_csv, conn, "WARNINGS",       "eng", "ita",       "TextWarning")

    conn.close()

    output_file_name = csv_file.replace(".csv", "_modificato.csv")

    # Rimuove \n e \r da tutte le stringhe del DataFrame
    df_csv = df_csv.applymap(lambda x: re.sub(r'[\r\n]+', '', x) if isinstance(x, str) else x)

    # Scrive il file con escapechar per evitare errori futuri
    df_csv.to_csv(
        output_file_name,
        index=False,
        encoding="utf-16",
        sep="\t",
        quoting=3,           # csv.QUOTE_NONE
        lineterminator="\r\n",
        escapechar="\\"
    )

    messagebox.showinfo("Completato", f"File aggiornato salvato:\n{output_file_name}")

def mostra_finestra():
    replace_text()
