📬 Bulk Certificate Mailer

A Python-based utility to generate and send personalized certificate emails in bulk — ideal for hackathons, DevFests, or campus events.
This project automates CSV cleaning, PDF attachment mapping, and email dispatching with Gmail SMTP.

⚠️ Security Reminder:
Never commit credentials (passwords, tokens, or app passwords).
Use environment variables or .env files excluded by .gitignore.

🧩 What’s Included
Script	Description
dedupe_names.py	Removes duplicate entries by name (case-insensitive).
attach_pdfs.py	Matches certificate PDFs to participant names in the CSV.
create_seed_csv.py	Creates a small CSV for testing the email workflow.
send_emails.py	Sends personalized HTML emails with attached PDFs. Supports --dry-run and --send.
⚙️ Installation

Clone the repository and install the required dependencies:

git clone https://github.com/<your-username>/bulk-certificate-mailer.git
cd bulk-certificate-mailer
python -m venv env
# Activate the virtual environment
# 📬 Bulk Certificate Mailer — example

This repository contains example scripts to prepare participant data and send personalized certificate emails in bulk. The README below is intentionally generic so you can adapt it for your event.

> ⚠️ Security reminder: Never commit secrets (passwords, tokens, or app passwords). Use environment variables or a local `.env` excluded by `.gitignore`.

---

## 🧩 What’s included

- `dedupe_names.py` — remove duplicate rows by `Name` (case-insensitive). Accepts `--input` and `--output` CLI flags.
- `attach_pdfs.py` — scan a folder for `.pdf` files and match them to names in the CSV; writes `*.with_pdfs.csv` with `PDF_Paths` and `PDF_Count` columns.
- `create_seed_csv.py` — create a small seed/test CSV for development and testing.
- `send_emails.py` — compose and send personalized HTML emails with attachments. Supports `--dry-run`, `--send`, and `--input` to point at a CSV.

---

## 🚀 Quick workflow

1. Export participant data (e.g., from Google Forms) and save as `input.csv`.
2. Remove duplicate names (keep first occurrence):

```powershell
python code/dedupe_names.py --input "input.csv" --output "dedup.csv"
```

3. Put certificate PDFs in a folder the attach script can scan (e.g. `./certificates/`).

4. Match PDFs to participants:

```powershell
python code/attach_pdfs.py
# creates code/dedup.with_pdfs.csv (or similar)
```

5. (Optional) Create a small seed/test CSV to try a live send:

```powershell
python code/create_seed_csv.py
# edit the generated seed CSV to add a valid PDF path if you want a real attachment
```

6. Dry-run the mailer (recommended):

```powershell
python code/send_emails.py --dry-run --input "code/dedup.with_pdfs.csv"
```

7. When ready, send for real (ensure SMTP credentials are set):

```powershell
python code/send_emails.py --send --input "code/dedup.with_pdfs.csv"
```

---

## ⚙️ Installation

Clone the repo and create a virtual environment:

```bash
git clone https://github.com/<your-username>/bulk-certificate-mailer.git
cd bulk-certificate-mailer
python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate
pip install -r requirements.txt
```

Example `requirements.txt` (adjust as needed):

```
pandas
python-dotenv
openpyxl
email-validator
```

---

## 📧 SMTP / Gmail setup

If you use Gmail, use an App Password (recommended):

1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Create an App Password: https://myaccount.google.com/apppasswords

Set credentials using environment variables (example PowerShell):

```powershell
$env:SMTP_HOST='smtp.gmail.com'
$env:SMTP_PORT='587'
$env:SMTP_USER='your_email@gmail.com'
$env:SMTP_PASS='your_app_password'
```

Or create a local `.env` file (do NOT commit it):

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

Notes:

- Google Workspace accounts may require admin approval for app passwords or SMTP relay.
- For other providers (Office365, SMTP relay, etc.) use the provider-specific host/port and credentials.

---

## 🧰 CLI Summary

- `dedupe_names.py -i <input.csv> -o <output.csv> [--show-sample]`
- `attach_pdfs.py` — scans for PDFs and writes `dedup.with_pdfs.csv`.
- `create_seed_csv.py` — creates a small `seed.csv` for testing (edit to add `PDF_Paths`).
- `send_emails.py --dry-run --input <path>` — prints recipients and attachments without sending.
- `send_emails.py --send --input <path>` — sends emails (requires SMTP configuration).

---

## 🔒 Safety & Best Practices

- Always run `--dry-run` first to verify recipients and attachments.
- Send in small batches to avoid provider rate limits — ask to add `--batch-size` and `--delay` support.
- Never store credentials in the repo; prefer environment variables or a secrets manager.
- Verify `PDF_Paths` point to existing files before sending.

---

## 🛠 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `SMTPAuthenticationError (535)` | Wrong credentials or provider blocking login | Use App Password for Gmail or correct credentials |
| `555 Syntax error` | Malformed recipient address (e.g., leading `@`) | Clean CSV or run `--dry-run` to find bad rows |
| Missing PDF | Incorrect path | Re-run `attach_pdfs.py` and check `PDF_Paths` |

---

## .gitignore recommendations

Add generated/test CSVs and local config to `.gitignore`:

```gitignore
# generated/test CSVs
code/test.csv
code/dedup.csv
code/dedup.with_pdfs.csv
code/seed.csv

# local secrets
.env

# python
__pycache__/
```

If any files are already tracked, remove them from the index then commit:

```powershell
git rm --cached "code/test.csv"
git rm --cached "code/dedup.csv"
git rm --cached "code/dedup.with_pdfs.csv"
git rm --cached "code/seed.csv"
git add code/.gitignore
git commit -m "Ignore generated CSVs and local config"
```

---

## ✨ Want improvements?

I can add features such as:

- `--batch-size` and `--delay` to control send rate.
- `--send-single` to test a single recipient live.
- Fuzzy name matching for `attach_pdfs.py` (RapidFuzz).
- Read SMTP config from environment variables if not already implemented.

Tell me which feature you'd like and I can implement it and run a test.
