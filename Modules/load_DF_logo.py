from PIL import Image, ImageTk
import tkinter as tk

import os
import sys

def carica_logo(larghezza=220, altezza=50, sfondo="#f0f4f8"):
    percorso_logo = resource_path("logo dragflow NL_335x70.png")

    try:
        img = Image.open(percorso_logo)
        img = img.resize((larghezza, altezza), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(img)

        def crea_label(parent):
            label = tk.Label(parent, image=logo, bg=sfondo, name="logo")
            label.image = logo  # evita che venga garbage collectato
            return label

        return crea_label
    except Exception as e:
        print(f"[ERRORE] Impossibile caricare il logo: {e}")

        def crea_label_placeholder(parent):
            return tk.Label(parent, text="[Logo mancante]", bg=sfondo, fg="red")

        return crea_label_placeholder



def resource_path(relative_path):
    """Ottiene il path assoluto, anche in eseguibile compilato."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)