import csv
import re
from pathlib import Path

BASE = Path("YOUr PATH HERE")
INPUT = Path("YOUr PATH HERE")
OUTPUT = INPUT.with_name(INPUT.stem + ".with_pdfs.csv")

def normalize(s: str) -> str:
    if s is None:
        return ""
    s = str(s)
    s = s.strip().lower()
    # remove stray dots before extension and collapse whitespace
    s = re.sub(r"[\.]+", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip()
    return s

# build map of normalized base filename -> list(paths)
pdf_map = {}
for p in BASE.glob("**/*.pdf"):
    base = normalize(p.stem)
    pdf_map.setdefault(base, []).append(str(p.resolve()))

# helper to try fuzzy matching if exact not found
def fuzzy_find(name_norm: str):
    # direct substring matches in pdf_map keys
    results = []
    for key, paths in pdf_map.items():
        if name_norm == key:
            return paths
    # try contains
    for key, paths in pdf_map.items():
        if name_norm in key or key in name_norm:
            results.extend(paths)
    # dedupe
    return list(dict.fromkeys(results))

with INPUT.open(newline='', encoding='utf-8-sig') as inf:
    reader = csv.DictReader(inf)
    rows = list(reader)
    if not rows:
        print('Input CSV is empty')
        raise SystemExit(1)
    fieldnames = reader.fieldnames if reader.fieldnames else []

# pick name column
name_col = None
for candidate in ['Name', 'Full Name', 'name', 'FullName']:
    if candidate in fieldnames:
        name_col = candidate
        break
if name_col is None:
    # fallback to first column
    name_col = fieldnames[0]
    print(f"Warning: couldn't find 'Name' column; using first column '{name_col}' as name")

out_fieldnames = list(fieldnames) + ['PDF_Paths', 'PDF_Count']
matched = 0
unmatched = []

with OUTPUT.open('w', newline='', encoding='utf-8') as outf:
    writer = csv.DictWriter(outf, fieldnames=out_fieldnames)
    writer.writeheader()
    for row in rows:
        raw_name = row.get(name_col, '')
        norm = normalize(raw_name)
        paths = pdf_map.get(norm)
        if not paths:
            paths = fuzzy_find(norm)
        if paths:
            row['PDF_Paths'] = ';'.join(paths)
            row['PDF_Count'] = str(len(paths))
            matched += 1
        else:
            row['PDF_Paths'] = ''
            row['PDF_Count'] = '0'
            unmatched.append(raw_name)
        writer.writerow(row)

print(f"Wrote: {OUTPUT}")
print(f"Total rows: {len(rows)}; Matched: {matched}; Unmatched: {len(unmatched)}")
if unmatched:
    print('\nSample unmatched names:')
    for n in unmatched[:20]:
        print('-', n)
