# gui.py
import tkinter as tk
from tkinter import messagebox

COLOR1 = "#ffffff"
COLOR2 = "#eaf3ff"

LARGH_TABLE_REF = 12
LARGH_TABLE_PAR = 10
LARGH_TABLE_DESC = 55
LARGH_TABLE_UNIT = 8
LARGH_TABLE_VAL_DB = 12
LARGH_TABLE_VAL_FILE = 12
LARGH_TABLE_IMPORT = 10

def mostra_finestra_diff(diff, db_path, scrivi_valori_callback):
    win = tk.Toplevel()
    win.title("Confronto parametri")
    win.geometry("900x600")
    win.configure(bg=COLOR1)

    top_frame = tk.Frame(win, bg=COLOR1)
    top_frame.pack(fill="x", padx=10)

    intestazioni = ["Tabella", "Parametro", "Descrizione", "Unità", "Valore DB", "Valore File", "Importa"]
    larghezze = [LARGH_TABLE_REF, LARGH_TABLE_PAR, LARGH_TABLE_DESC, LARGH_TABLE_UNIT, LARGH_TABLE_VAL_DB, LARGH_TABLE_VAL_FILE, LARGH_TABLE_IMPORT]

    for i, (txt, w) in enumerate(zip(intestazioni, larghezze)):
        tk.Label(top_frame, text=txt, bg=COLOR1, font=("Calibri", 10, "bold"), width=w).grid(row=0, column=i)

    canvas_frame = tk.Frame(win, bg=COLOR1)
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=0)

    canvas = tk.Canvas(canvas_frame, bg=COLOR1, highlightthickness=0)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner_frame = tk.Frame(canvas, bg=COLOR1)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    inner_frame.bind("<Configure>", update_scroll_region)

    var_map = []

    for i, (tab, key, descr, unit, old, new) in enumerate(diff):
        bg = COLOR1 if i % 2 == 0 else COLOR2

        tk.Label(inner_frame, text=tab, bg=bg, width=LARGH_TABLE_REF).grid(row=i, column=0)
        tk.Label(inner_frame, text=str(key), bg=bg, width=LARGH_TABLE_PAR).grid(row=i, column=1)
        tk.Label(inner_frame, text=str(descr), bg=bg, width=LARGH_TABLE_DESC, anchor="w").grid(row=i, column=2, sticky="w")
        tk.Label(inner_frame, text=str(unit), bg=bg, width=LARGH_TABLE_UNIT).grid(row=i, column=3)
        tk.Label(inner_frame, text=str(old), bg=bg, width=LARGH_TABLE_VAL_DB).grid(row=i, column=4)
        tk.Label(inner_frame, text=str(new), bg=bg, width=LARGH_TABLE_VAL_FILE).grid(row=i, column=5)

        # Centrare la checkbox in un frame
        var = tk.BooleanVar(value=True)
        container = tk.Frame(inner_frame, bg=bg, width=50, height=25)
        container.grid(row=i, column=6)
        container.grid_propagate(False)
        chk = tk.Checkbutton(container, variable=var, bg=bg)
        chk.pack(expand=True)
        
        var_map.append((var, tab, key, new))


    # Pulsanti in fondo
    def select_all():  [v.set(True) for v, _, _, _ in var_map]

    def deselect_all(): [v.set(False) for v, _, _, _ in var_map]

    def applica_modifiche():
        selezionati = [(tab, key, new) for var, tab, key, new in var_map if var.get()]
        scrivi_valori_callback(db_path, selezionati)
        messagebox.showinfo("Importazione completata", f"Importati {len(selezionati)} parametri nel database.")
        win.destroy()

    bottom_frame = tk.Frame(win, bg=COLOR1)
    bottom_frame.pack(pady=10)

    btn_width = 20
    btn_font = ("Calibri", 11)

    #Confirmation buttons
    btn_apply = tk.Button(bottom_frame, text="Applica selezione", command=applica_modifiche,
                            width=btn_width, font=btn_font, bg="#cce7ff")
    btn_apply.grid(row=0, column=0, padx=10)

    # Select/Deselect buttons
    btn_select = tk.Button(bottom_frame, text="Seleziona tutti", command=select_all,
                            width=btn_width, font=btn_font, bg="#d0f0c0")
    btn_select.grid(row=0, column=1, padx=10)

    btn_deselect = tk.Button(bottom_frame, text="Deseleziona tutti", command=deselect_all,
                            width=btn_width, font=btn_font, bg="#f0d0d0")
    btn_deselect.grid(row=0, column=2, padx=10)

    