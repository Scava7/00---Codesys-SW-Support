import tkinter as tk
from tkinter import messagebox
from Modules.DB_Excel import from_db_to_excel, from_excel_to_db
from Modules.HMI_Text import replace_HMI_texts
from Modules.IO_Struct import generate_IO_struct
from Modules.TXT_Generator import generate_txt

# Finestra principale
def main():
    root = tk.Tk()
    root.title("CODESYS SW SUPPORT")
    root.geometry("400x500")
    root.configure(bg="#f0f4f8")

    font_titolo = ("Calibri", 20, "bold")
    font_bottone = ("Calibri", 12)

    titolo = tk.Label(root, text="Tool Multiuso", font=font_titolo, bg="#f0f4f8", fg="#333")
    titolo.pack(pady=(20, 30))

    def aggiungi_bottone(testo, comando):
        b = tk.Button(root, text=testo, font=font_bottone, width=35, command=comando)
        b.pack(pady=8)

    # I seguenti comandi saranno collegati alle funzioni vere nei moduli
    aggiungi_bottone("From Database to Excel", from_db_to_excel.mostra_finestra)
    aggiungi_bottone("From Excel to Database", from_excel_to_db.mostra_finestra)
    aggiungi_bottone("Replace text in HMI project", replace_HMI_texts.mostra_finestra)
    aggiungi_bottone("Generate IO Struct", generate_IO_struct.mostra_finestra)
    aggiungi_bottone("Generate .txt for HMI and PLC", generate_txt.mostra_finestra)

    aggiungi_bottone("Esci", root.quit)

    root.mainloop()

if __name__ == "__main__":
    main()