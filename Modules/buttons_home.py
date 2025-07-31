from tkinter import messagebox
import tkinter as tk
from Modules.tooltip import Tooltip
from Modules.constants import *

PADX = (25, 0)
PADY = 8
ANCHOR = "w"

def crea_button_generico(testo, funzione, section_frame, font_bottone,
                         tooltip=None, db_path_var=None, richiede_db=False,
                         tabelle_controllo=None, monitor=None):
    
    frame = tk.Frame(section_frame, bg=COLORE_BG)
    frame.pack(pady=PADY, padx=PADX, anchor=ANCHOR)


    # Determina il colore e lo stato iniziale in base alla presenza del DB
    if richiede_db:
        if db_path_var and db_path_var.get():
            colore_iniziale = COLORE_PULSANTE_PREMIBILE
            stato_iniziale = "normal"
        else:
            colore_iniziale = COLORE_PULSANTE_NON_PREMIBILE
            stato_iniziale = "disabled"
    else:
        colore_iniziale = COLORE_PULSANTE_PREMIBILE
        stato_iniziale = "normal"


    b = tk.Button(frame, text=testo, font=font_bottone, fg=colore_testo_bottone,
              width=30, command=lambda: on_click(), bg=colore_iniziale, state=stato_iniziale)

    b.grid(row=0, column=0)

    if richiede_db:
        b.config(state="disabled")

    def on_click():
        db_path = db_path_var.get() if db_path_var else None
        if richiede_db and not db_path:
            messagebox.showerror("Errore", "Seleziona prima un file database.")
            return

        funzione(db_path) if richiede_db else funzione()

        # Colora di verde solo se il pulsante è monitorato
        if monitor and tabelle_controllo:
            monitor.aggiorna_hash_salvati(tabelle_controllo)

    if tooltip:
        punto_interrogativo = tk.Label(frame, text="?", font=("Calibri", 20, "bold"),
                                       fg="blue", bg=COLORE_BG, cursor="question_arrow")
        punto_interrogativo.grid(row=0, column=1, padx=(5, 0), sticky="w")
        Tooltip(punto_interrogativo, tooltip, border_color="#336699")

    # Abilita/disabilita dinamicamente in base alla selezione del DB
    if db_path_var and richiede_db:
        def aggiorna_stato(*args):
            path = db_path_var.get()
            if path:
                b.config(state="normal", bg=COLORE_PULSANTE_PREMIBILE)
            else:
                b.config(state="disabled", bg=COLORE_PULSANTE_NON_PREMIBILE)
        db_path_var.trace_add("write", aggiorna_stato)
        aggiorna_stato()

    # Registra nel monitor
    if monitor and tabelle_controllo:
        monitor.registra_pulsante(b, tabelle_controllo)
