import tkinter as tk
from tkinter import filedialog
from Modules.constants import*

def crea_selettore_database(parent, font_label):
    db_path_var = tk.StringVar()

    frame_principale = tk.Frame(parent, bg=COLORE_BG)
    frame_principale.pack(pady=(0, 20))

    # Riga 1: etichetta
    tk.Label(frame_principale, text="Percorso database:", font=font_label, fg=colore_testo_label, bg=COLORE_BG).pack(anchor="w")

    # Riga 2: campo + bottone
    frame_percorso = tk.Frame(frame_principale, bg=COLORE_BG)
    frame_percorso.pack()

    db_entry = tk.Entry(frame_percorso, textvariable=db_path_var, width=60)
    db_entry.pack(side="left", padx=(0, 5))

    def sfoglia_db():
        path = filedialog.askopenfilename(filetypes=[("Database SQLite", "*.db *.sqlite")])
        if path:
            db_path_var.set(path)

    tk.Button(frame_percorso, text="Sfoglia", command=sfoglia_db).pack(side="left")

    return db_path_var
