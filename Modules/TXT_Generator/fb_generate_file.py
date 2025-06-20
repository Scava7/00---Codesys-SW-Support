import sqlite3
import pandas as pd
import os
from datetime import datetime
from tkinter import filedialog, messagebox
from Modules.TXT_Generator.Text_blocks.fb_sts_block import sts_blocks
from Modules.TXT_Generator.Text_blocks.fb_hmi_cmd_blocks import hmi_cmd_blocks
from Modules.TXT_Generator.Text_blocks.fb_default_parameters import default_parameters_block
from Modules.TXT_Generator.Text_blocks.fb_actual_parameters import actual_par_block, actual_par_block_new
from Modules.TXT_Generator.constants import PLC, HMI
import os

def path_to_file(path_db, device):
    #nome_file = os.path.splitext(os.path.basename(path_db))[0] + f"_{device}.txt"
    
    # === ESTRAGGO NOME FILE BASE ===
    base_name = os.path.splitext(os.path.basename(path_db))[0]

    # === DATA E ORA ATTUALI ===
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M")  # es: "250617_0930"

    # === MODIFICA DEGLI ULTIMI 11 CARATTERI ===
    if len(base_name) >= 11:
        new_base = base_name[:-11] + timestamp
    else:
        new_base = base_name + "_" + timestamp  # fallback in caso sia troppo corto

    # === COSTRUZIONE NOME FILE ===
    file_name = f"{new_base}_{device}.txt"

    return(file_name)

def genera_file_txt(db_path, sts_tables, par_tables,hmi_cmd_tables, device, path_db, output_dir=None):
    conn = sqlite3.connect(db_path)
    contenuto = []

    # write the default parameters block only on PLC file
    if device == PLC:
        for nome_tabella, header_label in par_tables:
            df_par_bool = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
            blocco_default_par_bool = default_parameters_block(df_par_bool, header_label)
            contenuto.extend(blocco_default_par_bool)

    # write the actual paramaters block on both file (PLC and HMI)
    for nome_tabella, header_label in par_tables:
        df = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
        #act_par_block = actual_par_block(df, header_label, device)
        act_par_block = actual_par_block_new(df, header_label)
        contenuto.extend(act_par_block)

    # write the status block on both file (PLC and HMI)
    for nome_tabella, header_label in sts_tables:
        df = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
        blocco_status = sts_blocks(df, header_label, device)
        contenuto.extend(blocco_status)    

    # write the hmi cmd block on both file (PLC and HMI)
    for nome_tabella, header_label in hmi_cmd_tables:
        df = pd.read_sql_query(f"SELECT * FROM {nome_tabella}", conn)
        blocco_status = hmi_cmd_blocks(df, header_label, device)
        contenuto.extend(blocco_status)    

    conn.close()

    
    #insert HERE the function to generate the file name

    if output_dir:
        output_path = os.path.join(output_dir, path_to_file(path_db, device))
    else:
        output_path = path_to_file(path_db, device)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contenuto))

    print(f"[OK] File generato: {output_path}")
    messagebox.showinfo("Successo", f"File generato:\n{output_path}")
