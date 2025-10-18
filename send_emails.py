"""
Send personalized emails with attached PDFs listed in the CSV.
Usage:
  python send_emails.py --dry-run
  python send_emails.py --send

Environment variables (recommended):
  EMAIL_HOST - SMTP host (e.g., smtp.gmail.com)
  EMAIL_PORT - SMTP port (587 for TLS)
  EMAIL_USER - SMTP username (your email)
  EMAIL_PASS - SMTP password or app password

The script supports --dry-run to only print what it would send.
"""

import os
import csv
import argparse
import smtplib
import re
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

BASE = Path("YOUR PATH HERE")
DEFAULT_INPUT = BASE / "Your csv file here.csv"

# -------------------------
# Hardcoded SMTP / sender config
# Replace these values with your SMTP server, credentials and desired sender name/email.
# -------------------------
SMTP_HOST = 'smtp.host.com'       # e.g. 'smtp.gmail.com'
SMTP_PORT = 587                      # TLS port
SMTP_USER = 'example@gmail.com' # SMTP username
SMTP_PASS = 'Your SMTP password or app password'     # SMTP password or app password

# sender details (will default to SMTP_USER if not changed)
SENDER_NAME = 'SENDER NAME'
SENDER_EMAIL = SMTP_USER

# this is just a demo 

SUBJECT = "🚀 You Did It! Here’s Your Prompt with Gemini Certificate from DevFest Ranchi"
BODY_HTML = """
<p>Dear {name},</p>
<p>Congratulations! 🎉<br>
We’re delighted to share your e-certificate for successfully participating in the <strong>Prompt with Gemini</strong> initiative, conducted under the Google Student Ambassador Program at DevFest Ranchi.</p>
<p>📎 Please find your e-certificate attached to this email.</p>
<p>We’d love to see you celebrate your achievement on LinkedIn!<br>
When you share your certificate, don’t forget to mention our booth representatives —<br>
<strong><a href="https://www.linkedin.com/in/kriti-priya-9ba738279/" target="_blank" rel="noopener">Kriti Priya</a></strong> and <strong><a href="https://www.linkedin.com/in/tushar-kumar-mishra-1974b124b/" target="_blank" rel="noopener">Tushar Mishra</a></strong> — who made this initiative engaging and memorable.</p>                                                                                                  
<p>Thank you for being an enthusiastic part of the Google Student Ambassador Program and contributing to the success of this event.<br>
Keep exploring, keep creating, and keep learning with Gemini AI!</p>
<p>Warm regards,<br>
GSA Team Chhattisgarh<br>
Google Student Ambassador Program</p>
"""


def load_rows(input_path: Path):
    if not input_path.exists():
        raise SystemExit(f"Input CSV not found: {input_path}")
    with input_path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def make_message(sender_name, sender_email, recipient_name, recipient_email, subject, html_body, attachments):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = recipient_email
    msg.set_content('This is an HTML email. If you see this, your client does not support HTML.')
    msg.add_alternative(html_body, subtype='html')

    for path in attachments:
        p = Path(path)
        if not p.exists():
            print(f"Warning: attachment not found: {p}")
            continue
        maintype = 'application'
        subtype = 'pdf'
        with p.open('rb') as af:
            data = af.read()
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=p.name)
    return msg


def send_batch(rows, dry_run=True):
    # Use hardcoded SMTP config
    host = SMTP_HOST
    port = int(SMTP_PORT)
    user = SMTP_USER
    pwd = SMTP_PASS

    sender_name = SENDER_NAME
    sender_email = SENDER_EMAIL

    # try to detect the email column (common variants)
    fieldnames = rows[0].keys() if rows else []
    email_col = None
    for candidate in ('Email', 'Email id', 'Email ID', 'email', 'email id', 'email_id', 'Email_Id'):
        if candidate in fieldnames:
            email_col = candidate
            break
    if email_col is None:
        # fallback: find any column header that contains 'email'
        for h in fieldnames:
            if 'email' in h.lower():
                email_col = h
                break
    if email_col is None:
        print('Warning: could not detect an email column in the CSV headers. Available headers:')
        print(', '.join(fieldnames))
        valid = []
    else:
        # filter rows that have at least one plausible email
        def extract_emails(cell: str):
            if not cell:
                return []
            # split on common delimiters
            parts = [p.strip() for p in re.split(r'[;,\n/|]+| and ', cell) if p.strip()]
            # keep parts that look like email (contain @)
            return [p for p in parts if '@' in p]

        valid = []
        for r in rows:
            raw = r.get(email_col, '')
            emails = extract_emails(raw)
            if emails:
                # store normalized list back to row for later use
                r['_emails_parsed'] = emails
                valid.append(r)
    print(f"Total rows in CSV: {len(rows)}; with Email: {len(valid)} (detected column: {email_col})")

    if dry_run:
        print("--- DRY RUN: showing first 10 messages ---")
        for r in valid[:10]:
            name = r.get('Name', '').strip()
            emails = r.get('_emails_parsed') or []
            pdfs = [p for p in (r.get('PDF_Paths') or '').split(';') if p]
            print(f"To: {name} <{', '.join(emails)}>; Attachments: {len(pdfs)}")
        return

    if not host or not user or not pwd:
        raise SystemExit("SMTP_HOST, SMTP_USER and SMTP_PASS must be set in the script to send email")

    # open SMTP connection
    server = smtplib.SMTP(host, port)
    try:
        server.starttls()
        server.login(user, pwd)
        for r in valid:
            name = r.get('Name', '').strip()
            emails = r.get('_emails_parsed') or []
            pdfs = [p for p in (r.get('PDF_Paths') or '').split(';') if p]
            html = BODY_HTML.format(name=name)
            msg = make_message(sender_name, sender_email, name, ','.join(emails), SUBJECT, html, pdfs)
            try:
                server.send_message(msg)
                print(f"Sent: {', '.join(emails)} ({len(pdfs)} attachments)")
            except Exception as e:
                print(f"Failed to send to {', '.join(emails)}: {e}")
    finally:
        server.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Do not send mail; just show what would be sent')
    parser.add_argument('--send', action='store_true', help='Actually send the emails')
    parser.add_argument('--input', '-i', dest='input', help='Path to input CSV (overrides default)')
    args = parser.parse_args()

    # determine input CSV path: CLI -> ENV -> default
    if args.input:
        input_path = Path(args.input)
    else:
        input_path = Path(os.environ.get('EMAIL_INPUT')) if os.environ.get('EMAIL_INPUT') else DEFAULT_INPUT

    rows = load_rows(input_path)
    if args.send:
        send_batch(rows, dry_run=False)
    else:
        send_batch(rows, dry_run=True)
