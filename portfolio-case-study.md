# Portfolio Case Study: Mosser Cat Listing Alert Automation

## Project summary

I built a Python automation that monitors eBay for newly listed Mosser glass cat collectibles and sends an SMS alert when a new listing appears.

The project began as a personal collecting tool, but it was intentionally structured as a portfolio-ready automation case study. The same technical pattern can be adapted to business workflows such as CRM alerts, lead monitoring, inventory tracking, and deadline notifications.

## The problem

Rare collectible listings often appear unpredictably and can sell quickly. Manually checking eBay throughout the day is inefficient, distracting, and unreliable.

I wanted a system that could:

- search for relevant listings automatically
- identify only new results
- avoid duplicate notifications
- send a fast mobile alert
- be simple enough to maintain and expand

## The solution

The final MVP uses:

- Python for the automation logic
- eBay Browse API for listing search
- Twilio for SMS notifications
- a local JSON file for duplicate prevention
- environment variables for private credentials
- modular project files for maintainability

## Workflow

```text
Scheduled run
    ↓
Search eBay for "Mosser Cat"
    ↓
Normalize returned listings
    ↓
Load previously seen item IDs
    ↓
Compare current results against seen IDs
    ↓
Send SMS for new listings
    ↓
Save updated seen ID list
```

## Key technical decisions

### API-based search instead of scraping

Using the eBay API avoids fragile page-scraping logic and makes the project more stable, maintainable, and respectful of platform boundaries.

### Twilio SMS instead of email

SMS was chosen because the use case is time-sensitive. Rare listings may sell quickly, so mobile-first alerts are more useful than inbox notifications.

### Local JSON storage for MVP

A simple `seen_items.json` file is enough for the first version. It keeps the project lightweight while still demonstrating persistence and duplicate prevention.

### Modular architecture

The project is split into dedicated files:

- `ebay.py` for API search
- `notifier.py` for SMS formatting and sending
- `storage.py` for duplicate tracking
- `config.py` for environment variables
- `main.py` for orchestration

This makes the automation easier to test, debug, explain, and expand.

## Skills demonstrated

- REST API integration
- OAuth/client credentials flow
- Environment variable management
- JSON parsing
- SMS automation
- Duplicate detection
- Logging
- Python project organization
- Product thinking
- Workflow automation strategy

## Business translation

Although the project is personal, the automation pattern is directly transferable to professional operations.

The same architecture could be adapted to:

- notify a sales team when a new high-priority lead enters a CRM
- alert operations when a document is missing or overdue
- monitor incoming emails for urgent client requests
- track status changes in a workflow platform
- send daily summaries of new opportunities
- watch public listings or competitor activity

## Future roadmap

### Version 1.1

- Add price filters
- Improve SMS formatting
- Add better error handling

### Version 1.2

- Replace JSON with SQLite
- Track listing title, price, seller, and URL history
- Add daily summary reports

### Version 2.0

- Deploy to a cloud scheduler
- Add a small dashboard
- Add image analysis to classify glass color or detect reproductions
- Add scoring logic for potential deals

## Reflection

This project is a useful example of turning a personal pain point into a small, practical automation system. It shows how curiosity, domain knowledge, and technical tooling can combine to create something that is both personally useful and professionally relevant.
