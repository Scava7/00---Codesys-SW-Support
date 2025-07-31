import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import yaml
import os
import re

def scegli_file_xml():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Scegli un file XML",
        filetypes=[("File XML", "*.xml"), ("Tutti i file", "*.*")]
    )

def clean_type_name(type_name):
    if type_name.startswith("T_ARRAY__"):
        match = re.match(r"T_ARRAY__(\d+)__(\d+)__OF_(.+)", type_name)
        if match:
            start, end, base_type = match.groups()
            return f"ARRAY [{start}..{end}] OF {base_type}"
    if type_name.startswith("T_"):
        return type_name[2:]
    return type_name

def build_structure(type_definitions, type_name, visited=None):
    if visited is None:
        visited = set()
    if type_name in visited:
        return f"<recursive: {clean_type_name(type_name)}>"
    visited.add(type_name)

    if type_name not in type_definitions:
        return clean_type_name(type_name)

    result = {}
    for field in type_definitions[type_name]:
        result[field["name"]] = build_structure(type_definitions, field["type"], visited.copy())
    return result

def parse_nodes(xml_node, type_definitions, ns):
    result = {}
    for node in xml_node.findall('ns:Node', ns):
        node_name = node.get("name")
        node_type = node.get("type")
        if node_type:
            result[node_name] = build_structure(type_definitions, node_type)
        else:
            result[node_name] = parse_nodes(node, type_definitions, ns)

    for symbol in xml_node.findall('ns:Symbol', ns):
        var_name = symbol.get("name")
        var_type = symbol.get("type")
        result[var_name] = build_structure(type_definitions, var_type)

    return result

def converti_xml_in_yaml():
    file_path = scegli_file_xml()
    if not file_path:
        return

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        base_dir = os.path.dirname(file_path)
        ns = {'ns': 'http://www.3s-software.com/schemas/Symbolconfiguration.xsd'}

        type_definitions = {}
        for typedef in root.findall('.//ns:TypeUserDef', ns):
            typename = typedef.get("name")
            elements = []
            for el in typedef.findall('ns:UserDefElement', ns):
                elements.append({
                    'name': el.get("iecname"),
                    'type': el.get("type")
                })
            type_definitions[typename] = elements

        program_root = None
        for node in root.findall(".//ns:Node", ns):
            for child in node.findall("ns:Node", ns):
                if child.get("name") == "IO":
                    program_root = child
                    break
            if program_root:
                break

        if program_root is None:
            messagebox.showerror("Errore", "Nessun nodo 'IO' trovato nel file XML.")
            return

        output_tree = {"IO": parse_nodes(program_root, type_definitions, ns)}
        output_filename = os.path.join(base_dir, "IO_Struct.yaml")

        with open(output_filename, "w") as f:
            yaml.dump(output_tree, f, sort_keys=False, allow_unicode=True)

        messagebox.showinfo("Successo", f"File generato:\n{output_filename}")

    except Exception as e:
        messagebox.showerror("Errore", str(e))
