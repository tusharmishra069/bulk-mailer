import csv
from pathlib import Path

src = Path(__file__).parent / 'Sheet.csv'
out = Path(__file__).parent / 'Sheet.dedup.csv'

seen = set()
rows = []
with src.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    if fieldnames is None:
        raise SystemExit('No header found in CSV')
    for r in reader:
        name = (r.get('Name') or '').strip().lower()
        if name in seen or name == '':
            continue
        seen.add(name)
        rows.append(r)

with out.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Wrote {len(rows)} unique rows to: {out}')
print('Examples:')
for r in rows[:10]:
    print(r.get('Name'), '-', r.get('Email id'))
