import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from Modules.HMI_Text.copy_values import process_csv_same_lang, process_csv_events

# Percorso fisso del database (può essere reso variabile in futuro)
DB_PATH = r"C:\\Dev\\Copy text in HMI project\\SW_Support.sqlite"

def scegli_file_csv():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Seleziona il file CSV",
        filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
    )

def replace_text():
    csv_file = scegli_file_csv()
    if not csv_file:
        messagebox.showwarning("Nessun file selezionato", "Operazione annullata.")
        return

    df_csv = pd.read_csv(csv_file, encoding="utf-16", sep="\t", dtype=str)
    conn = sqlite3.connect(DB_PATH)

    # Processi
    process_csv_same_lang(df_csv, conn, "PAR BOOL",    "DESCRIPTION",      "TextParamDescriptionBool")
    process_csv_same_lang(df_csv, conn, "PAR INT",     "DESCRIPTION",      "TextParamDescriptionInt")
    process_csv_same_lang(df_csv, conn, "PAR INT",     "MEASURMENT_UNIT",  "TextParamUniMeasureInt")
    process_csv_events( df_csv, conn, "ALARMS",         "ENG", "ITA",       "TextAlarm")
    process_csv_events( df_csv, conn, "WARNINGS",       "ENG", "ITA",       "TextWarning")

    conn.close()

    output_file_name = csv_file.replace(".csv", "_modificato.csv")
    df_csv.to_csv(output_file_name, index=False, encoding="utf-16", sep="\t", quoting=3, lineterminator="\r\n")

    messagebox.showinfo("Completato", f"File aggiornato salvato:\n{output_file_name}")

def mostra_finestra():
    replace_text()
