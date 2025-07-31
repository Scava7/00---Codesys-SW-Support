
# Modules/table_monitor.py
import sqlite3
import hashlib
import json
from pathlib import Path
from Modules.constants import COLORE_PULSANTE_OK, COLORE_PULSANTE_PREMIBILE, COLORE_PULSANTE_NON_PREMIBILE

class TableMonitor:
    def __init__(self, root, db_path_var, refresh_interval_ms=2000):
        self.root = root
        self.db_path_var = db_path_var
        self.file_hash_salvati = "hash_tabelle.json"
        self.tabelle_salvate = self._carica_hash_salvati()
        self.tabelle_attuali = {}
        self.registrazioni = []  # [(button, [tabelle])]

        self.refresh_interval_ms = refresh_interval_ms
        self._loop()

    def _loop(self):
        self._aggiorna_hash_attuali()
        self._verifica_cambiamenti()
        self.root.after(self.refresh_interval_ms, self._loop)

    def _aggiorna_hash_attuali(self):
        db_path = self.db_path_var.get()
        if not db_path:
            # DB deselezionato → reset hash e disabilita pulsanti
            self.tabelle_attuali = {}
            for bottone, _ in self.registrazioni:
                bottone.config(state="disabled", bg=COLORE_PULSANTE_NON_PREMIBILE)
            return

        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tutte_le_tabelle = [r[0] for r in cur.fetchall()]

            for tabella in tutte_le_tabelle:
                cur.execute(f"SELECT * FROM {tabella}")
                dati = cur.fetchall()
                hash_val = hashlib.sha256(repr(dati).encode("utf-8")).hexdigest()
                self.tabelle_attuali[tabella] = hash_val

            conn.close()

            # Attiva i pulsanti ora che c'è un DB valido
            for bottone, _ in self.registrazioni:
                bottone.config(state="normal")

        except Exception as e:
            print(f"[Monitor] Errore nel calcolo hash: {e}")


    def _verifica_cambiamenti(self):
        if not self.db_path_var.get():
            return  # Nessun DB selezionato → esce
        for bottone, tabelle_da_controllare in self.registrazioni:
            stato = "ok"
            for tabella in tabelle_da_controllare:
                hash_attuale = self.tabelle_attuali.get(tabella)
                hash_salvato = self.tabelle_salvate.get(tabella)
                if hash_attuale and hash_attuale != hash_salvato:
                    stato = "changed"
                    break
            # Aggiorna il colore in base allo stato
            if stato == "ok":
                bottone.config(bg=COLORE_PULSANTE_OK)
            else:
                bottone.config(bg=COLORE_PULSANTE_PREMIBILE)

    def registra_pulsante(self, bottone, tabelle_da_controllare):
        self.registrazioni.append((bottone, tabelle_da_controllare))

    def aggiorna_hash_salvati(self, tabelle):
        for tabella in tabelle:
            h = self.tabelle_attuali.get(tabella)
            if h:
                self.tabelle_salvate[tabella] = h
        self._salva_hash()

    def _carica_hash_salvati(self):
        Path(self.file_hash_salvati).touch(exist_ok=True)
        try:
            with open(self.file_hash_salvati, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _salva_hash(self):
        with open(self.file_hash_salvati, "w") as f:
            json.dump(self.tabelle_salvate, f, indent=2)
