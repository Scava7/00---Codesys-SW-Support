# parser.py
import re

def parse_txtrecipe(path):
    with open(path, "r", encoding="utf-8") as f:
        righe = [r.strip() for r in f if r.strip()]

    bool_lines, int_lines, mach_lines = [], [], []
    mode = None
    for line in righe[1:]:
        if "_Parameters.PAR_BOOL[" in line:
            mode = "bool"
        elif "_Parameters.PAR_INT[" in line:
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
        match = re.search(r"\[(\d+)\]\s*:=\s*(TRUE|FALSE|-?\d+)", line, re.IGNORECASE)
        if not match:
            return (None, None)
        index = int(match.group(1))
        value_raw = match.group(2).upper()
        return (index, value_raw if value_raw in ["TRUE", "FALSE"] else int(value_raw))

    param_bool = dict(parse_line(l) for l in bool_lines)
    param_int = dict(parse_line(l) for l in int_lines)
    param_mach = dict(zip(["A", "B", "C", "D"], mach_lines))
    return param_bool, param_int, param_mach
