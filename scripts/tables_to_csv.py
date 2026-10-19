r"""Convert the LaTeX result tables (tables/S_*.tex) into plain CSV files.

Entries such as $(5.884\pm0.186){\times}10^{-4}$ become two columns (value, err);
entries such as $-0.240\,(16)$ (paired difference with 95% CI half-width in units
of the last digit) become value=-0.240, err=0.016.
"""
import csv, re, sys, pathlib

PM  = re.compile(r"\(([-+\d.]+)\\pm([\d.]+)\)\{\\times\}10\^\{(-?\d+)\}")
SCI = re.compile(r"([-+\d.]+)\{\\times\}10\^\{(-?\d+)\}")
PAR = re.compile(r"([-+]?[\d.]+)\\,\((\d+)\)")

def clean_header(h):
    h = h.replace("\\rm", "").replace("\\,", "")
    h = re.sub(r"[\$\{\}\\]", "", h).strip().replace("__", "_")
    return h.replace(" ", "_").replace("__", "_")

def parse_cell(c):
    c = c.strip().strip("$").strip()
    m = PM.fullmatch(c)
    if m:
        s = 10.0 ** int(m.group(3))
        return [float(m.group(1)) * s, float(m.group(2)) * s]
    m = SCI.fullmatch(c)
    if m:
        return [float(m.group(1)) * 10.0 ** int(m.group(2))]
    m = PAR.fullmatch(c)
    if m:
        val = m.group(1)
        dec = len(val.split(".")[1]) if "." in val else 0
        return [float(val), int(m.group(2)) * 10.0 ** (-dec)]
    m = re.fullmatch(r"10\^\{(-?\d+)\}", c)
    if m:
        return [10.0 ** int(m.group(1))]
    try:
        return [float(c)]
    except ValueError:
        return [c]

def convert(tex, out):
    body = pathlib.Path(tex).read_text()
    body = re.sub(r"\\begin\{tabular\}\{[^}]*\}|\\end\{tabular\}|\\hline", "", body)
    rows = [r.strip() for r in body.split("\\\\") if "&" in r]
    header = [clean_header(h) for h in rows[0].split("&")]
    data = [[parse_cell(c) for c in r.split("&")] for r in rows[1:]]
    two = [any(len(row[j]) == 2 for row in data) for j in range(len(header))]
    cols = []
    for h, t in zip(header, two):
        cols += [h, h + "_err"] if t else [h]
    with open(out, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for row in data:
            line = []
            for cell, t in zip(row, two):
                line += cell + ([""] if t and len(cell) == 1 else [])
            w.writerow([f"{x:.6g}" if isinstance(x, float) else x for x in line])

if __name__ == "__main__":
    src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "tables")
    dst = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "data")
    dst.mkdir(exist_ok=True)
    for t in sorted(src.glob("S_*.tex")):
        convert(t, dst / (t.stem + ".csv"))
        print("wrote", dst / (t.stem + ".csv"))
