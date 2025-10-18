#!/usr/bin/env python3
"""
Create a seed CSV for testing mail sending. Copies headers from the existing dedup.with_pdfs CSV and writes a single-row CSV with the requested test email.
"""
from pathlib import Path
import csv

SRC = Path('D:/gdg/dev fest/code/Devfest Ranchi - Sheet2.dedup.with_pdfs.csv')
OUT = SRC.with_name('Devfest Ranchi - Sheet2.seed.csv')

if not SRC.exists():
    raise SystemExit(f"Source CSV not found: {SRC}")

with SRC.open(newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames if reader.fieldnames else []

# prepare seed row using headers
seed = {h: '' for h in headers}
seed['Name'] = 'Tushar Mishra'
# detect the email header (common variants)
email_col = None
for candidate in ('Email', 'Email id', 'Email ID', 'email', 'email id', 'email_id', 'Email_Id'):
    if candidate in headers:
        email_col = candidate
        break
if email_col is None:
    for h in headers:
        if 'email' in h.lower():
            email_col = h
            break
if email_col is None:
    # fallback to add a column
    headers.append('Email')
    email_col = 'Email'

seed[email_col] = 'tusharmishra069@gmail.com'
# attach a fake pdf path for testing (optional):
seed['PDF_Paths'] = ''
seed['PDF_Count'] = '0'

with OUT.open('w', newline='', encoding='utf-8') as out:
    writer = csv.DictWriter(out, fieldnames=headers)
    writer.writeheader()
    writer.writerow(seed)

print(f"Wrote seed CSV: {OUT}")
