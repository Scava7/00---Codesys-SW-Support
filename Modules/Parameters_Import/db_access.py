# db_access.py
import sqlite3

def leggi_valori_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("SELECT n, factory_value FROM PAR_BOOL")
    db_bool = dict(cur.fetchall())
    cur.execute("SELECT n, factory_value FROM PAR_INT")
    db_int = dict(cur.fetchall())
    cur.execute("SELECT n, factory_value FROM MACH_DETAILS")
    db_mach = dict(cur.fetchall())

    cur.execute("SELECT n, description FROM PAR_BOOL")
    desc_bool = dict(cur.fetchall())
    cur.execute("SELECT n, description FROM PAR_INT")
    desc_int = dict(cur.fetchall())
    cur.execute("SELECT n, description FROM MACH_DETAILS")
    desc_mach = dict(cur.fetchall())

    cur.execute("SELECT n, measurment_unit FROM PAR_INT")
    unit_int = dict(cur.fetchall())

    con.close()
    return {
        "bool": db_bool, "int": db_int, "mach": db_mach,
        "desc_bool": desc_bool, "desc_int": desc_int, "desc_mach": desc_mach,
        "unit_int": unit_int
    }

def scrivi_valori(db_path, modifiche):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    for tab, key, val in modifiche:
        cur.execute(f"UPDATE {tab} SET factory_value = ? WHERE n = ?", (val, key))
    con.commit()
    con.close()
