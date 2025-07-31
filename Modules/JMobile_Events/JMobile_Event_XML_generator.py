import xml.etree.ElementTree as ET
import os
import sqlite3
import copy
import traceback
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from xml.dom import minidom

def genera_allarmi_xml(db_path_var):

    print(f"Tipo di db_path_var: {type(db_path_var)}")

    try:
        # Finestra per selezionare il file di partenza
        input_file = askopenfilename(
            filetypes=[("XML files", "*.xml")],
            title="Seleziona il file ExportedAlarms.xml"
        )
        if not input_file:
            return  # Utente ha annullato

        template_path = r"C:\Dev\00 - Codesys SW Support\Modules\JMobile_Events\JMobile_Event_Template.xml"
        template_event = ET.parse(template_path).getroot()


        # Carica il file XML di partenza e rimuovi tutti gli <alarm>
        tree = ET.parse(input_file)
        root = tree.getroot()
        for alarm in root.findall("alarm"):
            root.remove(alarm)

        # Connessione al database
        if not os.path.exists(db_path_var):
            messagebox.showerror("Errore", f"Database non trovato:\n{db_path_var}")
            return
        conn = sqlite3.connect(db_path_var)
        cursor = conn.cursor()

        # Carica dati da entrambe le tabelle
        cursor.execute("SELECT eng FROM WARNINGS WHERE eng IS NOT NULL AND TRIM(eng) <> ''")
        warnings = cursor.fetchall()

        cursor.execute("SELECT eng FROM ALARMS WHERE eng IS NOT NULL AND TRIM(eng) <> ''")
        alarms = cursor.fetchall()

        conn.close()

        def create_event(array, desc, nome, severity):
            new_event = copy.deepcopy(template_event)
            new_event.find("name").text = nome
            new_event.find("severity").text = str(severity)
            new_event.find("source").text = str(f"HMI_Codesys/Application/IO/Event/Sts/{array}")
            # trova il nodo <description>/<L1>
            descr_node = new_event.find("description/L1")
            if descr_node is not None:
                descr_node.text = str(desc)
            return new_event

        # Crea allarmi per i WARNINGS
        for i, (desc,) in enumerate(warnings, start=0):
            nome = f"WARNING{i:03}"
            array = f"Warning[{i}]"
            nuovo_alarm = create_event(array, desc, nome, severity=1)
            root.append(nuovo_alarm)

        # Crea allarmi per gli ALARMS
        for i, (desc,) in enumerate(alarms, start=0):
            nome = f"ALARM{i:03}"
            array = f"Alarm[{i}]"
            nuovo_alarm = create_event(array, desc, nome, severity=6)
            root.append(nuovo_alarm)

        # Salva il file aggiornato
        output_path = os.path.join(os.path.dirname(input_file), "UpdatedAlarms.xml")
        
        # Converte in stringa e formatta con indentazione
        rough_string = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="    ")

        # Rimuove le righe vuote
        cleaned_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip() != ""])

        # Salva su file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_xml)

        messagebox.showinfo("Successo", f"File aggiornato salvato come:\n{output_path}")

    except Exception as e:
        traceback.print_exc()  # <-- stampa traccia completa nel terminale
        messagebox.showerror("Errore", f"Errore durante la generazione del file XML:\n{str(e)}")


#genera_allarmi_xml(r"C:\Scambio\2025\2500058-2500193 (DPP400 - HY400+2XEXHY35 - Noleggio - Italia)\SW_SUPPORT\2500058_250610_1456.sqlite")