import os
import subprocess

# Percorso completo del file da aprire
file_path = r"C:\Scambio\2024\2402094 - Technosub DRH\SW_Support\Sw_Support_TECHNOSUB_250718_1349_HMI.txt"

# Percorso Notepad++
npp_path = r"C:\Program Files\Notepad++\notepad++.exe"

# Prima prova con Notepad++
if os.path.exists(npp_path):
    subprocess.run([npp_path, file_path])
else:
    print("Notepad++ non trovato, uso Notepad.")
    subprocess.run(["notepad.exe", file_path])
