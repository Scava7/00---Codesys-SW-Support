import tkinter as tk
from tkinter import messagebox, filedialog
from Modules.DB_Excel import from_db_to_excel, from_excel_to_db
from Modules.HMI_Text import replace_HMI_texts
from Modules.IO_Struct import generate_IO_struct
from Modules.TXT_Generator import generate_txt

def main():
    root = tk.Tk()
    root.title("CODESYS SW SUPPORT")
    root.geometry("500x600")
    root.configure(bg="#aed7ff")

    font_titolo = ("Calibri", 20, "bold")
    font_bottone = ("Calibri", 12)
    font_label = ("Calibri", 10)

    titolo = tk.Label(root, text="Tool Multiuso", font=font_titolo, bg="#f0f4f8", fg="#333")
    titolo.pack(pady=(20, 20))

    # === CAMPO PERCORSO DB ===
    db_frame = tk.Frame(root, bg="#b7dafd")
    db_frame.pack(pady=(0, 20))

    db_path_var = tk.StringVar()

    def sfoglia_db():
        path = filedialog.askopenfilename(filetypes=[("Database SQLite", "*.db *.sqlite")])
        if path:
            db_path_var.set(path)

    tk.Label(db_frame, text="Percorso database:", font=font_label, bg="#f0f4f8").pack(side="left", padx=(0,5))
    db_entry = tk.Entry(db_frame, textvariable=db_path_var, width=40)
    db_entry.pack(side="left", padx=(0,5))
    tk.Button(db_frame, text="Sfoglia", command=sfoglia_db).pack(side="left")

    # === AGGIUNGI I BOTTONI ===
    def aggiungi_bottone(testo, funzione):
        def wrapper():
            db_path = db_path_var.get()
            if not db_path and testo != "Esci":
                messagebox.showerror("Errore", "Seleziona prima un file database.")
                return
            funzione(db_path)  # Passa il percorso come argomento
        b = tk.Button(root, text=testo, font=font_bottone, width=35, command=wrapper)
        b.pack(pady=8)

    # Questi moduli devono ora accettare `db_path` come argomento
    aggiungi_bottone("From Database to Excel", from_db_to_excel.mostra_finestra)
    aggiungi_bottone("From Excel to Database", from_excel_to_db.mostra_finestra)
    aggiungi_bottone("Replace text in HMI project", replace_HMI_texts.mostra_finestra)
    aggiungi_bottone("Generate IO Struct", generate_IO_struct.mostra_finestra)
    aggiungi_bottone("Generate .txt for HMI and PLC", generate_txt.mostra_finestra)

    aggiungi_bottone("Esci", root.quit)

    root.mainloop()

if __name__ == "__main__":
    main()
