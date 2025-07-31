import tkinter as tk
from tkinter import ttk

from Modules.load_DF_logo import carica_logo
from Modules.select_DB import crea_selettore_database

from Modules.buttons_home import add_button, add_button_no_db
from Modules.DB_Excel.from_db_to_excel import esporta_sqlite_in_excel
from Modules.DB_Excel.from_excel_to_db import importa_excel_in_sqlite
from Modules.HMI_Text.replace_HMI_texts import replace_text
from Modules.IO_Struct.generate_IO_struct import converti_xml_in_yaml
from Modules.TXT_Generator.generate_txt import genera_txt
from Modules.JMobile_Events.JMobile_Event_XML_generator import genera_allarmi_xml

def main():
    root = tk.Tk()
    root.title("CODESYS SW SUPPORT")
    root.geometry("500x700")
    root.configure(bg="#f0f4f8")

    font_titolo = ("Calibri", 20, "bold")
    font_label = ("Calibri", 10)
    font_bottone = ("Calibri", 12)

    # Logo
    logo_label_fn = carica_logo()
    logo_label = logo_label_fn(root)
    logo_label.pack(pady=(10, 10))

    # Titolo
    titolo = tk.Label(root, text="Tool Multiuso", font=font_titolo, bg="#f0f4f8", fg="#333")
    titolo.pack(pady=(10, 30))

    # Campo percorso database
    db_path_var = crea_selettore_database(root, font_label)

    # === SEZIONE: PULSANTI CON DATABASE =============================================================================================================================
    db_section_frame = tk.Frame(root, bg="#f0f4f8")
    db_section_frame.pack(pady=(10, 10))

    tooltip_text = "Questa funzione permette di generare due file TXT con i dati del database selezionato. Un file dovrà essere copiato nel progetto PLC, l'altro nel progetto HMI."
    add_button("Generate TXT", genera_txt, db_path_var, db_section_frame, font_bottone, tooltip_text)

    tooltip_text = "Genera un file XML con gli eventi del pannello Codesys, commestibile da JMobile."
    add_button("Generate JMobile Event XML", genera_allarmi_xml, db_path_var, db_section_frame, font_bottone, tooltip_text)

    # Separatore
    ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

    # === SEZIONE: PULSANTI SENZA DATABASE ===========================================================================================================================
    no_db_section_frame = tk.Frame(root, bg="#f0f4f8", )
    no_db_section_frame.pack(pady=(10, 10))

    tooltip_text = "Questa funzione permette di esportare i dati del database in un file Excel."
    add_button_no_db("From Database to Excel", esporta_sqlite_in_excel, no_db_section_frame, font_bottone, tooltip_text)
    
    tooltip_text = "Questa funzione permette di importare i dati da un file Excel in un database SQLite."
    add_button_no_db("From Excel to Database", importa_excel_in_sqlite, no_db_section_frame, font_bottone, tooltip_text)

    tooltip_text = "Questa funzione permette di sostituire i testi in un progetto HMI. è necessario esportare il .csv da CODESYS prima di utilizzarla."
    add_button_no_db("Replace text in HMI project", replace_text, no_db_section_frame, font_bottone, tooltip_text)

    tooltip_text = "Questa funzione permette trasformare il file XML generato da CODESYS in una struttura ad albero per una migliore visualizzazione."
    add_button_no_db("Generate IO Struct", converti_xml_in_yaml, no_db_section_frame, font_bottone, tooltip_text)

    # Separatore
    ttk.Separator(root, orient='horizontal').pack(fill='x', pady=10)

    # === SEZIONE: USCITA ===========================================================================================================================================
    exit_frame = tk.Frame(root, bg="#f0f4f8")
    exit_frame.pack(pady=(10, 10))

    tk.Button(exit_frame, text="Esci", font=font_bottone, width=35, command=root.quit).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
