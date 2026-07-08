# Mosser Cat eBay Alert Bot

A small Python automation that searches eBay for newly listed **Mosser Cat** glass listings and sends an SMS alert through Twilio when a new result appears.

This project was designed as both a practical collecting tool and a portfolio-ready automation case study.

## What it does

1. Searches eBay for a configured keyword, such as `Mosser Cat`.
2. Sorts results by newly listed.
3. Compares current listings against a local `seen_items.json` file.
4. Sends an SMS alert for listings that have not been seen before.
5. Saves notified item IDs so duplicate alerts are avoided.

## Why this project matters

This is a focused automation project that demonstrates:

- API authentication
- REST API calls
- JSON parsing
- Environment variable management
- SMS notification workflows
- Duplicate detection
- Logging
- Lightweight persistence
- Portfolio documentation

## Project structure

```text
mosser-cat-alert/
├── main.py              # Entry point
├── ebay.py              # eBay API functions
├── notifier.py          # Twilio SMS formatting and sending
├── storage.py           # Seen-item persistence
├── config.py            # Environment-based settings
├── requirements.txt     # Python dependencies
├── .env.example         # Template for local secrets
├── seen_items.json      # Local item ID memory
└── README.md            # Documentation
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Mac/Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

Copy the example file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```bash
Copy-Item .env.example .env
```

Then fill in:

```text
EBAY_CLIENT_ID=
EBAY_CLIENT_SECRET=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=
TO_PHONE_NUMBER=
```

## Running the bot

### Test without sending SMS

```bash
python main.py --dry-run --notify-existing
```

### Normal run

```bash
python main.py
```

## Scheduling options

For a first version, run it manually while testing.

Later, it can be scheduled with:

- Windows Task Scheduler
- macOS/Linux cron
- GitHub Actions
- Railway
- Render
- a Raspberry Pi or always-on computer

A practical MVP schedule would be every 5-15 minutes.

## Portfolio case study angle

### Problem

Rare Mosser glass cat listings can sell quickly, and manually refreshing eBay is inefficient.

### Solution

Build a lightweight automation that monitors eBay search results and sends real-time SMS alerts when new listings appear.

### Outcome

The bot reduces manual checking, helps surface time-sensitive collecting opportunities, and demonstrates a repeatable automation pattern that can be adapted for business workflows.

### Transferable business use cases

The same architecture could monitor:

- new franchise leads
- high-intent form submissions
- CRM status changes
- urgent client emails
- new support tickets
- expiring document deadlines
- competitor listing changes
- inventory changes

## Future improvements

- Add price thresholds.
- Add category filtering.
- Store listings in SQLite instead of JSON.
- Deploy to Railway or Render.
- Add a daily digest.
- Add image analysis for glass color identification.
- Add seller reputation scoring.
- Add Discord or email alerts.
- Build a simple dashboard.
