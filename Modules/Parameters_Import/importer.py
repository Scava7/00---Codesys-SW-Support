# importer.py
from tkinter import filedialog, messagebox
from .parser import parse_txtrecipe
from .db_access import leggi_valori_db, scrivi_valori
from .gui import mostra_finestra_diff

def import_parameters_file(db_path):
    path = filedialog.askopenfilename(filetypes=[("Parameters Recipe", "*.txtrecipe")], title="Seleziona file")
    if not path:
        return

    try:
        param_bool, param_int, param_mach = parse_txtrecipe(path)
        db = leggi_valori_db(db_path)

        diff = []
        for k, v in param_bool.items():
            if db["bool"].get(k) != v:
                diff.append(("PAR_BOOL", k, db["desc_bool"].get(k, ""), "", db["bool"].get(k), v))
        for k, v in param_int.items():
            if db["int"].get(k) != v:
                diff.append(("PAR_INT", k, db["desc_int"].get(k, ""), db["unit_int"].get(k, ""), db["int"].get(k), v))
        for k, v in param_mach.items():
            if db["mach"].get(k) != v:
                diff.append(("MACH_DETAILS", k, db["desc_mach"].get(k, ""), "", db["mach"].get(k), v))

        if not diff:
            messagebox.showinfo("Importazione", "Nessuna differenza trovata tra il file e il database.")
            return

        mostra_finestra_diff(diff, db_path, scrivi_valori)

    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante l'importazione: {e}")
