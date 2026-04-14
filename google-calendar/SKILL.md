---
name: google-calendar
description: Interact with Google Calendar via the Google Calendar API – list upcoming events, create new events, update or delete them. Use this skill when you need programmatic access to your calendar from OpenClaw.
---

# Google Calendar Skill

## Overview
This skill provides a thin wrapper around the Google Calendar REST API. It lets you:
- **list** upcoming events (optionally filtered by time range or query)
- **add** a new event with title, start/end time, description, location, and attendees
- **update** an existing event by its ID
- **delete** an event by its ID

The skill is implemented in Python (`scripts/google_calendar.py`). It expects the following environment variables to be set (you can store them securely with `openclaw secret set`):
```
GOOGLE_CALENDAR_ID=primary   # or the ID of a specific calendar
```

## Python Environment
If this skill runs Python code, use a dedicated virtual environment at `./.venv` in the skill root so its dependencies do not interfere with other skills.

- All Python-related commands for this skill must be run from the skill root: `~/.openclaw/skills/google-calendar`
- Always `cd ~/.openclaw/skills/google-calendar` before creating the environment, installing dependencies, or running scripts
- Create it with `python3 -m venv .venv`
- Run Python scripts with `./.venv/bin/python`
- Run package installs with `./.venv/bin/pip`
- Install dependencies into this environment only
- Never use `python`, `python3`, `pip`, or `pip3` directly for this skill after the venv exists
- Do not rely on global site-packages or another skill's virtual environment

Example:
```bash
cd ~/.openclaw/skills/google-calendar
./.venv/bin/python scripts/google_calendar.py --help
```

Authentication can be configured in any one of these ways:

```bash
# Preferred on servers: Google Service Account
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Standard user OAuth
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REFRESH_TOKEN=...

# Legacy fallback
GOOGLE_ACCESS_TOKEN=...
```

Authentication priority is:
1. `GOOGLE_APPLICATION_CREDENTIALS`
2. `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` + `GOOGLE_REFRESH_TOKEN`
3. `GOOGLE_ACCESS_TOKEN`

## Commands
```
google-calendar list [--from <ISO> --to <ISO> --max <N>]
google-calendar add   --title <title> [--start <ISO> --end <ISO>]
                     [--desc <description> --location <loc> --attendees <email1,email2>]
google-calendar update --event-id <id> [--title <title> ... other fields]
google-calendar delete --event-id <id>
```
All commands return a JSON payload printed to stdout. Errors are printed to stderr and cause a non‑zero exit code.

## Authentication Setup

### Option A: Service Account
Use this on servers or automations where you want headless access without user consent screens.

1. **Create a Google Cloud project** and enable the *Google Calendar API*.
2. **Create a service account** and download its JSON key.
3. **Share the target calendar** with the service account email and grant the required permissions.
4. Store the credentials path and calendar ID:
   ```bash
   openclaw secret set GOOGLE_APPLICATION_CREDENTIALS /absolute/path/to/service-account.json
   openclaw secret set GOOGLE_CALENDAR_ID primary
   ```

### Option B: User OAuth
Use this when the calendar should be accessed as a real Google user.

1. **Create a Google Cloud project** and enable the *Google Calendar API*.
2. **Create OAuth credentials** (type *Desktop app*). Note the `client_id` and `client_secret`.
3. Use the refresh helper to mint an access token when needed, or obtain a refresh token through your existing OAuth flow:
   ```bash
   cd ~/.openclaw/skills/google-calendar
   GOOGLE_CLIENT_ID=... \
   GOOGLE_CLIENT_SECRET=... \
   GOOGLE_REFRESH_TOKEN=... \
   ./.venv/bin/python scripts/refresh_token.py
   ```
4. Store the credentials securely:
   ```bash
   openclaw secret set GOOGLE_CLIENT_ID <value>
   openclaw secret set GOOGLE_CLIENT_SECRET <value>
   openclaw secret set GOOGLE_REFRESH_TOKEN <value>
   openclaw secret set GOOGLE_CALENDAR_ID primary
   ```

### Option C: Direct Access Token
Use only if another process already refreshes `GOOGLE_ACCESS_TOKEN` for you.

```bash
openclaw secret set GOOGLE_ACCESS_TOKEN <value>
openclaw secret set GOOGLE_CALENDAR_ID primary
```

## Dependencies

Create the skill-local virtual environment, then install the required Python packages into it:
   ```bash
   cd ~/.openclaw/skills/google-calendar
   python3 -m venv .venv
   ./.venv/bin/pip install google-auth google-auth-oauthlib google-api-python-client
   ```

## How it works (brief)
The script talks directly to the Google Calendar REST API over HTTP. It resolves an access token from one of the supported auth modes, attaches it as a Bearer token, and calls the appropriate Calendar API endpoint.

## References
- Google Calendar API reference: https://developers.google.com/calendar/api/v3/reference
- OAuth 2.0 for installed apps: https://developers.google.com/identity/protocols/oauth2/native-app
- Service accounts: https://cloud.google.com/iam/docs/service-accounts-overview

---

**Note:** This skill does not require a GUI; it works entirely via HTTP calls, so it is suitable for headless servers.
