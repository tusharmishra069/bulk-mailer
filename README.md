# 📬 Bulk Mailer

A Python-based utility to generate and send personalized emails in bulk — ideal for hackathons, DevFests, or campus events.

This project automates CSV cleaning, PDF attachment mapping, and email dispatching with Gmail SMTP.

---

## ⚠️ Security Reminder

**Never commit credentials (passwords, tokens, or app passwords).**  
Use environment variables or a `.env` file (which should be excluded by `.gitignore`).

---

## 🧩 What’s Included

| Script                | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `dedupe_names.py`     | Removes duplicate entries by name (case-insensitive).              |
| `attach_pdfs.py`      | Matches PDFs to participant names in the CSV.                      |
| `create_seed_csv.py`  | Creates a small CSV for testing the email workflow.                |
| `send_emails.py`      | Sends personalized HTML emails with attached PDFs.<br>Supports `--dry-run` and `--send`. |

---

## 🚀 Quick Workflow

1. **Export participant data** (e.g., from Google Forms) and save as `input.csv`.

2. **Remove duplicate names:**
    ```sh
    python code/dedupe_names.py --input "input.csv" --output "dedup.csv"
    ```

3. **Place PDFs** in a folder (e.g., `./attachments/`).

4. **Match PDFs to participants:**
    ```sh
    python code/attach_pdfs.py
    # creates code/dedup.with_pdfs.csv
    ```

5. **(Optional) Create a small test CSV:**
    ```sh
    python code/create_seed_csv.py
    ```

6. **Dry-run the mailer:**
    ```sh
    python code/send_emails.py --dry-run --input "code/dedup.with_pdfs.csv"
    ```

7. **Send for real (ensure SMTP credentials are set):**
    ```sh
    python code/send_emails.py --send --input "code/dedup.with_pdfs.csv"
    ```

---

## ⚙️ Installation

Clone the repo and set up your environment:

```sh
git clone https://github.com/<your-username>/bulk-mailer.git
cd bulk-mailer
python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate
pip install -r requirements.txt
```

**Example `requirements.txt`:**
```
pandas
python-dotenv
openpyxl
email-validator
```

---

## 📧 SMTP / Gmail Setup

If using Gmail, create an App Password:

1. **Enable 2-Step Verification:**  
   [https://myaccount.google.com/security](https://myaccount.google.com/security)

2. **Create an App Password:**  
   [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

Set credentials via **environment variables**:
```sh
export SMTP_HOST='smtp.gmail.com'
export SMTP_PORT='587'
export SMTP_USER='your_email@gmail.com'
export SMTP_PASS='your_app_password'
```

Or use a **`.env` file**:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

---

## 🧰 CLI Summary

| Command                                                        | Description                                   |
|----------------------------------------------------------------|-----------------------------------------------|
| `dedupe_names.py -i <input.csv> -o <output.csv>`               | Removes duplicates.                           |
| `attach_pdfs.py`                                               | Scans for PDFs and writes dedup.with_pdfs.csv.|
| `create_seed_csv.py`                                           | Creates seed.csv for testing.                 |
| `send_emails.py --dry-run --input <path>`                      | Prints recipients and attachments.            |
| `send_emails.py --send --input <path>`                         | Sends emails (requires SMTP config).          |

---

## 🔒 Safety & Best Practices

- Always run `--dry-run` first.
- Send in small batches to avoid rate limits.
- **Never store credentials in the repo.**
- Verify all `PDF_Path` values before sending.

---

## 🛠 Troubleshooting

| Error                       | Cause                | Fix                         |
|-----------------------------|----------------------|-----------------------------|
| SMTPAuthenticationError 535 | Invalid credentials  | Use App Password            |
| 555 Syntax error            | Malformed email      | Clean CSV and re-run dry-run|
| Missing PDF                 | Invalid file path    | Re-run attach_pdfs.py       |

---

## 🗂️ .gitignore Recommendations

```
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

To remove already tracked files:

```sh
git rm --cached "code/test.csv"
git rm --cached "code/dedup.csv"
git rm --cached "code/dedup.with_pdfs.csv"
git rm --cached "code/seed.csv"
git add code/.gitignore
git commit -m "Ignore generated CSVs and local config"
```

---

## ✨ Future Improvements

Potential enhancements:

- `--batch-size` and `--delay` support
- `--send-single` for one-off tests
- Fuzzy name matching using [RapidFuzz](https://github.com/maxbachmann/RapidFuzz)
- Auto-read SMTP config from `.env`

---
