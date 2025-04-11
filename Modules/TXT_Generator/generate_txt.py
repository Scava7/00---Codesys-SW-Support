import os
import sqlite3
from tkinter import filedialog, messagebox
from Modules.TXT_Generator.fb_generate_file import genera_file_txt
from Modules.TXT_Generator.constants import PLC, HMI

def scegli_file():
    return filedialog.askopenfilename(
        title="Seleziona il database SQLite",
        filetypes=[("Database SQLite", "*.sqlite *.db")]
    )

def genera_txt():
    path_db = scegli_file()
    if not path_db:
        messagebox.showwarning("Attenzione", "Nessun file selezionato.")
        return
    if not os.path.exists(path_db):
        messagebox.showerror("Errore", "File non trovato.")
        return

    sts_tables = [
        ("mach_sts_bool", "STS BOOL"),
        ("mach_sts_int", "STS INT"),
        ("mach_sts_dint", "STS DINT"),
    ]

    par_tables = [
        ("par_bool", "PAR BOOL"),
        ("par_int", "PAR INT"),
    ]

    try:
        genera_file_txt(path_db, sts_tables=sts_tables, par_tables=par_tables, device=PLC, path_db=path_db)
        genera_file_txt(path_db, sts_tables=sts_tables, par_tables=par_tables, device=HMI, path_db=path_db)
    except Exception as e:
        messagebox.showerror("Errore", str(e))
        return

    messagebox.showinfo("Successo", "File TXT generati correttamente.")

def mostra_finestra():
    genera_txt()
