from tkinter import messagebox, filedialog
import tkinter as tk
from Modules.tooltip import Tooltip 


def add_button(testo, funzione, db_path_var, section_frame, font_bottone, tooltip=None):
        def wrapper():
            db_path = db_path_var.get()
            if not db_path:
                messagebox.showerror("Errore", "Seleziona prima un file database.")
                return
            funzione(db_path)

        frame = tk.Frame(section_frame, bg="#f0f4f8")
        frame.pack(pady=8)
        b = tk.Button(frame, text=testo, font=font_bottone, width=30, command=wrapper)
        b.pack(side="left")

        if tooltip:
            punto_interrogativo = tk.Label(frame, text="?", font=("Calibri", 20, "bold"),
                                        fg="blue", bg="#f0f4f8", cursor="question_arrow")
            punto_interrogativo.pack(side="left", padx=5)
            Tooltip(punto_interrogativo, tooltip, border_color="#336699")


def add_button_no_db(testo, funzione, section_frame, font_bottone, tooltip=None):
        frame = tk.Frame(section_frame, bg="#f0f4f8")
        frame.pack(pady=8)
        b = tk.Button(frame, text=testo, font=font_bottone, width=30, command=funzione)
        b.pack(side="left")
        if tooltip:
            punto_interrogativo = tk.Label(frame, text="?", font=("Calibri", 20, "bold"),
                                        fg="blue", bg="#f0f4f8", cursor="question_arrow")
            punto_interrogativo.pack(side="left", padx=5)
            Tooltip(punto_interrogativo, tooltip, border_color="#336699")