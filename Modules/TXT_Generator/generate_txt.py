import os
import sqlite3
from tkinter import filedialog, messagebox
from Modules.TXT_Generator.fb_generate_file import genera_file_txt, open_generated_files
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

    base_dir = os.path.dirname(path_db)

    sts_tables = [
        ("mach_sts_bool", "STS BOOL"),
        ("mach_sts_int", "STS INT"),
        ("mach_sts_dint", "STS DINT"),
    ]

    par_tables = [
        ("par_bool", "PAR BOOL"),
        ("par_int", "PAR INT"),
    ]

    hmi_cmd_tables = [
        ("hmi_cmd_bool", "HMI COMMANDS BOOL"),
        ("hmi_cmd_int", "HMI COMMANDS INT"),
    ]

    try:
        file_paths = []
        file_paths.append(genera_file_txt(path_db, sts_tables=sts_tables, par_tables=par_tables,hmi_cmd_tables=hmi_cmd_tables, device=PLC, path_db=path_db, output_dir=base_dir))
        file_paths.append(genera_file_txt(path_db, sts_tables=sts_tables, par_tables=par_tables,hmi_cmd_tables=hmi_cmd_tables, device=HMI, path_db=path_db, output_dir=base_dir))
    
        open_generated_files(file_paths)
            
    except Exception as e:
        messagebox.showerror("Errore", str(e))
        return

    messagebox.showinfo("Successo", "File TXT generati correttamente.")

def mostra_finestra():
    genera_txt()
