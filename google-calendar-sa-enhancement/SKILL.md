---
name: google-calendar-sa-enhancement
description: "Documents the process of enhancing the 'google-calendar' OpenClaw skill to support Google Service Account authentication, addressing initial limitations with user OAuth credentials. This skill details the required code modifications to 'google_calendar.py' and environment variable setup for seamless integration with service accounts."
---

# Google Calendar Service Account Enhancement

## Overview
This skill documents the process of modifying the default `google-calendar` OpenClaw skill to allow authentication using a Google Service Account (SA) instead of the standard user OAuth flow (Client ID, Client Secret, Refresh Token).

The original `google-calendar` skill's Python script (`scripts/google_calendar.py`) expected `GOOGLE_ACCESS_TOKEN` (obtained via a separate `google_calendar.auth` script or pre-set) for authentication. This enhancement allows the skill to directly leverage `GOOGLE_APPLICATION_CREDENTIALS` for service account based access.

## Problem Statement
The default `google-calendar` skill, while functional, primarily relies on user OAuth credentials. When a service account with calendar write permissions is available (via `GOOGLE_APPLICATION_CREDENTIALS`), the skill does not natively support this authentication method, leading to `ModuleNotFoundError` or `Invalid authentication credentials` errors when attempting to use service account tokens directly.

## Solution: Code Modification to `google_calendar.py`

The core of this enhancement involves modifying the `get_access_token()` function within `scripts/google_calendar.py` to first attempt service account authentication.

### File to Modify
`/home/ubuntu/.openclaw/workspace/skills/google-calendar/scripts/google_calendar.py`

### Required Imports (add to top of the file)
```python
from google.auth import load_credentials_from_file
from google.auth.transport.requests import Request
```

### Scope Definition (add near `BASE_URL`)
```python
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar']
```
These scopes are necessary for the service account to interact with the Calendar API.

### Modified `get_access_token()` Function
Replace the original `get_access_token()` function with the following:
```python
def get_access_token():
    # Try service account first if GOOGLE_APPLICATION_CREDENTIALS is set
    sa_credential_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if sa_credential_path and os.path.exists(sa_credential_path):
        try:
            # Load credentials from the service account key file with specified scopes
            creds, _ = load_credentials_from_file(sa_credential_path, scopes=SCOPES)
            # Refresh credentials to get a fresh access token
            creds.refresh(Request())
            return creds.token
        except Exception as e:
            sys.stderr.write(f'Warning: Service account token refresh failed: {e}\n')
            # Fall through to GOOGLE_ACCESS_TOKEN if service account fails or is not correctly configured
            pass

    # Fallback to direct GOOGLE_ACCESS_TOKEN (for user OAuth flow)
    token = os.getenv('GOOGLE_ACCESS_TOKEN')
    if not token:
        sys.stderr.write('Error: GOOGLE_ACCESS_TOKEN env var not set and service account not configured or failed.\n')
        sys.exit(1)
    return token
```

### Rationale for Modification
This modified function prioritizes authentication using the service account key file specified by `GOOGLE_APPLICATION_CREDENTIALS`. If the service account path is provided and valid, it attempts to obtain an access token using it. If that fails (e.g., due to incorrect path, permissions, or missing file) or if `GOOGLE_APPLICATION_CREDENTIALS` is not set, it gracefully falls back to looking for `GOOGLE_ACCESS_TOKEN` (the original skill's expected method).

## Environment Setup for Service Account

To use the enhanced `google-calendar` skill with a service account, ensure the following environment variables are set during execution:

*   **`GOOGLE_APPLICATION_CREDENTIALS`**: Path to your Google Service Account JSON key file (e.g., `/home/ubuntu/.openclaw/workspace/.env.d/google-sa.json`). This variable is crucial for the modified `get_access_token()` function to find your service account credentials.
*   **`GOOGLE_CALENDAR_ID`**: The ID of the target Google Calendar (e.g., `pcqmm1c4m079mqrgu1o4bu8vno@group.calendar.google.com`).

### Example Usage (After Modification)

Once `google_calendar.py` is modified, you can use `exec` with the appropriate environment variables:

```bash
/home/ubuntu/.openclaw/workspace/.venvs/google-calendar-test/bin/python /home/ubuntu/.openclaw/workspace/skills/google-calendar/scripts/google_calendar.py add \ 
  --title "Your Event Title" \ 
  --start "2026-01-01T09:00:00+08:00" \ 
  --end "2026-01-01T17:00:00+08:00" \ 
  --desc "Event Description"
```
And set the environment variables via the `env` parameter in the `exec` tool call:
```python
env = {
    "GOOGLE_APPLICATION_CREDENTIALS": "/home/ubuntu/.openclaw/workspace/.env.d/google-sa.json",
    "GOOGLE_CALENDAR_ID": "pcqmm1c4m079mqrgu1o4bu8vno@group.calendar.google.com"
}
```

## Prerequisites

*   **`google-calendar` skill installed**: `npx clawhub@latest install google-calendar`
*   **Python Virtual Environment**: A Python 3 environment (e.g., `/home/ubuntu/.openclaw/workspace/.venvs/google-calendar-test/`)
*   **Required Python Packages**: `pip install google-auth google-auth-oauthlib google-api-python-client` (already installed in the specified venv).
*   **Google Cloud Service Account**: A service account with the necessary Calendar API permissions, and its JSON key file.
*   **Calendar ID**: The specific Google Calendar ID to interact with.
