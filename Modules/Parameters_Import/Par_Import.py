import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import hashlib
import re

def import_parameters_file(db_path):
    path = filedialog.askopenfilename(
        filetypes=[("Parameters Recipe", "*.txtrecipe")],
        title="Seleziona un file Parameters.txtrecipe"
    )
    if not path:
        return

    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        with open(path, "r", encoding="utf-8") as f:
            righe = [r.strip() for r in f if r.strip()]

        timestamp = righe[0]
        bool_lines = []
        int_lines = []
        mach_lines = []

        mode = None
        for line in righe[1:]:
            if "_Parameters.PAR_bool[" in line:
                mode = "bool"
            elif "_Parameters.PAR_int[" in line:
                mode = "int"
            elif re.match(r'^[^:=\[\]]+$', line) and ":" not in line:
                mode = "mach"
            if mode == "bool":
                bool_lines.append(line)
            elif mode == "int":
                int_lines.append(line)
            elif mode == "mach":
                mach_lines.append(line)

        def parse_line(line):
            match = re.search(r"\[(\d+)\]\s*:=\s*(-?\d+)", line)
            return (int(match.group(1)), int(match.group(2))) if match else (None, None)

        param_bool = dict(parse_line(l) for l in bool_lines)
        param_int = dict(parse_line(l) for l in int_lines)
        param_mach = dict(zip(["A", "B", "C", "D"], mach_lines))

        cur.execute("SELECT n, factory_value FROM PAR_BOOL")
        db_bool = dict(cur.fetchall())
        cur.execute("SELECT n, factory_value FROM PAR_INT")
        db_int = dict(cur.fetchall())
        cur.execute("SELECT n, factory_value FROM MACH_DETAILS")
        db_mach = dict(cur.fetchall())

        diff = []

        for k, v in param_bool.items():
            if db_bool.get(k) != v:
                diff.append(("PAR_BOOL", k, db_bool.get(k), v))
        for k, v in param_int.items():
            if db_int.get(k) != v:
                diff.append(("PAR_INT", k, db_int.get(k), v))
        for k, v in param_mach.items():
            if db_mach.get(k) != v:
                diff.append(("MACH_DETAILS", k, db_mach.get(k), v))

        if not diff:
            messagebox.showinfo("Importazione", "Nessuna differenza trovata tra il file e il database.")
            return

        # GUI di selezione
        win = tk.Toplevel()
        win.title("Confronto parametri")
        win.geometry("700x500")
        win.configure(bg="#ffffff")

        frame = tk.Frame(win, bg="#ffffff")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(frame, bg="#ffffff")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ffffff")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scroll_frame, text="Tabella", bg="#ffffff", font=("Calibri", 10, "bold"), width=15).grid(row=0, column=0)
        tk.Label(scroll_frame, text="Parametro", bg="#ffffff", font=("Calibri", 10, "bold"), width=15).grid(row=0, column=1)
        tk.Label(scroll_frame, text="Valore DB", bg="#ffffff", font=("Calibri", 10, "bold"), width=15).grid(row=0, column=2)
        tk.Label(scroll_frame, text="Valore File", bg="#ffffff", font=("Calibri", 10, "bold"), width=15).grid(row=0, column=3)
        tk.Label(scroll_frame, text="Importa", bg="#ffffff", font=("Calibri", 10, "bold"), width=10).grid(row=0, column=4)

        var_map = []

        for i, (tab, key, old, new) in enumerate(diff, start=1):
            tk.Label(scroll_frame, text=tab, bg="#ffffff").grid(row=i, column=0)
            tk.Label(scroll_frame, text=str(key), bg="#ffffff").grid(row=i, column=1)
            tk.Label(scroll_frame, text=str(old), bg="#ffffff").grid(row=i, column=2)
            tk.Label(scroll_frame, text=str(new), bg="#ffffff").grid(row=i, column=3)
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(scroll_frame, variable=var, bg="#ffffff")
            chk.grid(row=i, column=4)
            var_map.append((var, tab, key, new))

        def applica_modifiche():
            count = 0
            for var, tab, key, new in var_map:
                if var.get():
                    if tab == "PAR_BOOL" or tab == "PAR_INT":
                        cur.execute(f"UPDATE {tab} SET factory_value = ? WHERE n = ?", (new, key))
                        count += 1
                    elif tab == "MACH_DETAILS":
                        cur.execute("UPDATE MACH_DETAILS SET factory_value = ? WHERE n = ?", (new, key))
                        count += 1
            con.commit()
            messagebox.showinfo("Importazione completata", f"Importati {count} parametri nel database.")
            win.destroy()

        tk.Button(win, text="Applica selezione", command=applica_modifiche, font=("Calibri", 12), bg="#cce7ff").pack(pady=10)

    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante l'importazione: {e}")
    finally:
        try:
            con.close()
        except:
            pass
