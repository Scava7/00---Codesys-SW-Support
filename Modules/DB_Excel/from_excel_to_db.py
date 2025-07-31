import os
import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox

def scegli_file(titolo, tipi_file):
    file_path = filedialog.askopenfilename(title=titolo, filetypes=tipi_file)
    return file_path

def scegli_salvataggio(titolo, tipo_file):
    file_path = filedialog.asksaveasfilename(title=titolo, defaultextension=tipo_file[1], filetypes=[tipo_file])
    return file_path

def is_file_locked(filepath):
    try:
        with open(filepath, 'rb+'):
            return False
    except IOError:
        return True

def importa_excel_in_sqlite():
    xlsx_path = scegli_file("Scegli il file Excel", [("Excel Workbook", "*.xlsx")])
    if not xlsx_path:
        return

    if is_file_locked(xlsx_path):
        messagebox.showerror("Errore", "Il file Excel è aperto o bloccato. Chiudilo prima di continuare.")
        return

    db_path = scegli_salvataggio("Salva il database SQLite", ("Database SQLite", ".sqlite"))
    if not db_path:
        return

    xls = pd.ExcelFile(xlsx_path)
    conn = sqlite3.connect(db_path)

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

        if sheet_name == "PAR_BOOL" and "factory_value" in df.columns:
            df["factory_value"] = df["factory_value"].apply(lambda x: "TRUE" if str(x).strip().upper() == "TRUE" else "FALSE")

        df.to_sql(sheet_name, conn, index=False, if_exists="replace")

    conn.close()
    messagebox.showinfo("Completato", f"Importazione completata in:\n{db_path}")

