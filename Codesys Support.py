import tkinter as tk
from tkinter import ttk

from Modules.load_DF_logo import carica_logo
from Modules.select_DB import crea_selettore_database

from Modules.buttons_home import crea_button_generico
from Modules.DB_Excel.from_db_to_excel import esporta_sqlite_in_excel
from Modules.DB_Excel.from_excel_to_db import importa_excel_in_sqlite
from Modules.HMI_Text.replace_HMI_texts import replace_text
from Modules.IO_Struct.generate_IO_struct import converti_xml_in_yaml
from Modules.TXT_Generator.generate_txt import genera_txt
from Modules.JMobile_Events.JMobile_Event_XML_generator import genera_allarmi_xml
from Modules.Ash_Calc.table_monitor import TableMonitor
from Modules.Parameters_Import.importer import import_parameters_file
from Modules.constants import *


def main():
    root = tk.Tk()
    root.title("CODESYS SW SUPPORT")
    root.geometry("500x800")
    root.configure(bg=COLORE_BG)

    # Logo
    logo_label_fn = carica_logo()
    logo_label = logo_label_fn(root)
    logo_label.configure(bg=COLORE_BG) 
    logo_label.pack(pady=(10, 10))

    # Titolo
    titolo = tk.Label(root, text="Tool Multiuso", font=font_titolo, bg=COLORE_BG, fg="#333")
    titolo.pack(pady=(10, 30))

    db_path_var = tk.StringVar()
    monitor = TableMonitor(root, db_path_var, refresh_interval_ms=2000)
    crea_selettore_database(root, font_label, db_path_var, monitor=monitor)


    # === SEZIONE: PULSANTI CON DATABASE =============================================================================================================================
    db_section_frame = tk.Frame(root, bg=COLORE_BG)
    db_section_frame.pack(pady=(10, 10))

    tooltip_text = "Questa funzione permette di generare due file TXT con i dati del database selezionato. Un file dovrà essere copiato nel progetto PLC, l'altro nel progetto HMI."
    crea_button_generico("Generate TXT", genera_txt, db_section_frame, font_bottone,
                         tooltip=tooltip_text, db_path_var=db_path_var, richiede_db=True,
                         tabelle_controllo=["PAR_INT", "PAR_BOOL"], monitor=monitor)

    tooltip_text = "Questa funzione permette di leggere un file Parameters.txtrecipe esportato dall'HMI e confrontare i dati attuali con quelli del database. Successivamente l'utente può scegliere se aggiornare il database con i nuovi valori."
    crea_button_generico("Import actual parameters", import_parameters_file, db_section_frame, font_bottone,
                         tooltip=tooltip_text, db_path_var=db_path_var, richiede_db=True,
                         tabelle_controllo=[], monitor=None)

    tooltip_text = "Questa funzione permette di sostituire i testi in un progetto HMI. È necessario esportare il .csv da CODESYS prima di utilizzarla."
    crea_button_generico("Replace text in HMI project", replace_text, db_section_frame, font_bottone,
                         tooltip=tooltip_text, db_path_var=db_path_var, richiede_db=True,
                         tabelle_controllo=["ALARMS", "WARNINGS", "PAR_INT", "PAR_BOOL"], monitor=monitor)
    
    tooltip_text = "Genera un file XML con gli eventi del pannello Codesys, commestibile da JMobile."
    crea_button_generico("Generate JMobile Event XML", genera_allarmi_xml, db_section_frame, font_bottone,
                         tooltip=tooltip_text, db_path_var=db_path_var, richiede_db=True,
                         tabelle_controllo=["ALARMS", "WARNINGS"], monitor=monitor)
    
    tooltip_text = "Questa funzione permette di esportare i dati del database in un file Excel."
    crea_button_generico("From Database to Excel", esporta_sqlite_in_excel, db_section_frame, font_bottone,
                         tooltip=tooltip_text, db_path_var=db_path_var, richiede_db=True,
                         tabelle_controllo=["ALARMS", "WARNINGS", "PAR_INT", "PAR_BOOL", "HMI_CMD_BOOL", "HMI_CMD_INT", "MACH_DETAILS","MACH_STS_BOOL","MACH_STS_DINT","MACH_STS_INT"], monitor=monitor)

    # Separatore
    ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

    # === SEZIONE: PULSANTI SENZA DATABASE ===========================================================================================================================
    no_db_section_frame = tk.Frame(root, bg=COLORE_BG)
    no_db_section_frame.pack(pady=(10, 10))

    tooltip_text = "Questa funzione permette di importare i dati da un file Excel in un database SQLite."
    crea_button_generico("From Excel to Database", importa_excel_in_sqlite, no_db_section_frame, font_bottone,
                         tooltip=tooltip_text)

    tooltip_text = "Questa funzione permette di trasformare il file XML generato da CODESYS in una struttura ad albero per una migliore visualizzazione."
    crea_button_generico("Generate IO Struct", converti_xml_in_yaml, no_db_section_frame, font_bottone,
                         tooltip=tooltip_text)

    # Separatore
    ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

    # === SEZIONE: USCITA ============================================================================================================================================
    exit_frame = tk.Frame(root, bg=COLORE_BG)
    exit_frame.pack(pady=(10, 10))

    tk.Button(exit_frame, text="Esci", font=font_bottone, width=30,
              bg=COLORE_PULSANTE_ESCI_ATTIVO, activebackground=COLORE_PULSANTE_ESCI_PREMUTO,
              command=root.quit).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
