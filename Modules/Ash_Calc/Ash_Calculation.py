import sqlite3
import hashlib
import json
from pathlib import Path

HASH_PATH = "stato_tabella_hash.json"

def calcola_hash_tabella(db_path, tabella):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabella}")
        rows = cur.fetchall()
        conn.close()
        return hashlib.sha256(repr(rows).encode("utf-8")).hexdigest()
    except Exception as e:
        print(f"Errore nel calcolo hash: {e}")
        return None

def salva_hash_tabella(chiave, valore):
    Path(HASH_PATH).touch(exist_ok=True)
    try:
        with open(HASH_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}

    data[chiave] = valore
    with open(HASH_PATH, "w") as f:
        json.dump(data, f)

def carica_hash_tabella(chiave):
    try:
        with open(HASH_PATH, "r") as f:
            data = json.load(f)
        return data.get(chiave)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
