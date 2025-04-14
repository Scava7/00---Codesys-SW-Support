import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox

def scegli_file(titolo, tipi_file):
    file_path = filedialog.askopenfilename(title=titolo, filetypes=tipi_file)
    return file_path

def scegli_salvataggio(titolo, tipo_file):
    file_path = filedialog.asksaveasfilename(title=titolo, defaultextension=tipo_file[1], filetypes=[tipo_file])
    return file_path

def importa_excel_in_sqlite():
    xlsx_path = scegli_file("Scegli il file Excel", [("Excel Workbook", "*.xlsx")])
    if not xlsx_path:
        return

    db_path = scegli_salvataggio("Salva il database SQLite", ("Database SQLite", ".sqlite"))
    if not db_path:
        return

    xls = pd.ExcelFile(xlsx_path)
    conn = sqlite3.connect(db_path)

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Rimuove spazi da tutte le stringhe
        df.to_sql(sheet_name, conn, index=False, if_exists="replace")

    conn.close()
    messagebox.showinfo("Completato", f"Importazione completata in:\n{db_path}")

def mostra_finestra():
    importa_excel_in_sqlite()
