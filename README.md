# Email Outreach Tool

A simple Python tool to automate cold email outreach.

## Features

- **`email_scrapper.py`** – Scrapes email addresses from a webpage. Stores results in `emails-output.csv` *(auto-ignored via `.gitignore`)*  
- **`email_sender.py`** – Sends a templated email (with optional attachment) to each contact in `emails.csv`. Email body must be writtin inside `email-body.txt`.

## Setup

1. **Clone the repo**

```bash
https://github.com/aDiThYa-808/email-outreach-tool.git
cd email-outreach-tool
```

2. **Create a `.env` file**

```
SENDER_EMAIL=you@example.com  
EMAIL_PASSWORD=yourpassword
```

3. **Install dependencies**

```bash
pip install python-dotenv
```
4. **Create required files**

```bash
touch emails.csv
touch email-body.txt
touch emails-output.csv
touch failed_emails.log
```

6. **Run the scripts**

```bash
# To scrape emails
python email_scrapper.py

# To send emails
python email_sender_leads.py
```

## Files that you must create after cloning
- `emails.csv`: contains the list of email addresses (in the first row) 
- `email-body.txt`: contains body of the email
- `poster.jpeg`/`poster.png`: image to add as attachment
- `failed_emails.log`: to keep track of failed emails
- `emails-output`: store scrapped emails

## Notes
- `emails.csv` and `emails-output.csv` are `.gitignored` to avoid leaking data.
- Batch size and delay can be configured in `email_sender.py` to avoid rate limits or blacklisting.
