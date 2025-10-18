🚀 Bulk Mailer

This repository automates the process of preparing participant data and sending personalized certificate emails with attached PDF certificates.

⚠️ Important:
This project deals with real email sending. Never commit secrets or credentials. Use environment variables for all sensitive information.

📦 Features

dedupe_names.py — Removes duplicate rows (case-insensitive) by participant name.

attach_pdfs.py — Matches .pdf certificates to names in the CSV and outputs a new CSV with attachment paths.

create_seed_csv.py — Generates a small sample CSV for safe test runs.

send_emails.py — Sends personalized HTML emails with PDF attachments. Supports dry-run and real send modes.

⚙️ Installation

Clone the repository and install dependencies:

git clone https://github.com/yourusername/bulk-certificate-mailer.git
cd bulk-certificate-mailer
python -m venv env
source env/bin/activate   # on Windows: env\Scripts\activate
pip install -r requirements.txt


Example requirements.txt:

pandas
python-dotenv
smtplib
email
openpyxl

🧭 Quick Workflow

Prepare your master CSV (e.g. exported from Google Forms) and name it participants.csv.

Remove duplicates:

python code/dedupe_names.py --input participants.csv --output participants.dedup.csv


Place all participant certificate PDFs under a common folder, e.g.:

/path/to/project/certificates/


Match PDFs to CSV entries:

python code/attach_pdfs.py
# produces participants.dedup.with_pdfs.csv


(Optional) Create a test CSV for trial emails:

python code/create_seed_csv.py


Perform a dry run (no actual emails sent):

python code/send_emails.py --dry-run --input participants.dedup.with_pdfs.csv


Send actual emails (once verified):

python code/send_emails.py --send --input participants.dedup.with_pdfs.csv

📧 SMTP / Gmail Setup

Do not use your normal Gmail password. Use an App Password.

Steps:

Enable 2-Step Verification: https://myaccount.google.com/security

Create an App Password: https://myaccount.google.com/apppasswords

Set environment variables before running:

export SMTP_HOST='smtp.gmail.com'
export SMTP_PORT='587'
export SMTP_USER='your_email@gmail.com'
export SMTP_PASS='your_app_password'


Then run:

python code/send_emails.py --send --input participants.dedup.with_pdfs.csv

🧠 Script CLI Summary
Script	Description
dedupe_names.py -i <input.csv> -o <output.csv>	Removes duplicate participant names
attach_pdfs.py	Links certificate PDFs to rows in the deduped CSV
create_seed_csv.py	Creates a small testing CSV
send_emails.py --dry-run --input <csv>	Simulates email send
send_emails.py --send --input <csv>	Sends actual emails (requires SMTP credentials)
🔒 Safety Tips

Always start with --dry-run.

Keep credentials in environment variables, never in code.

Send in batches if handling hundreds of recipients.

Check for missing PDF paths before sending.

🧰 Optional Enhancements

You can extend this tool to include:

--batch-size and --delay for throttled sending

--send-single to test one recipient

Fuzzy matching (using RapidFuzz) for better name-to-PDF detection

Full .env configuration for SMTP credentials

🧾 Git Ignore

Ensure .gitignore excludes generated and sensitive files:

code/*.csv
.env
__pycache__/
*.log

🛠 Troubleshooting
Error	Likely Cause	Fix
SMTPAuthenticationError (535)	Wrong credentials	Use App Password
555 Syntax error	Bad email address in CSV	Clean up entries
Missing PDFs	Incorrect paths	Check output of attach_pdfs.py