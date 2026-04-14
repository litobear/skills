#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

from google.auth import load_credentials_from_file
from google.auth.transport.requests import Request

BASE_URL = 'https://www.googleapis.com/calendar/v3'
SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar',
]


def get_service_account_token():
    sa_credential_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not sa_credential_path:
        return None
    if not os.path.exists(sa_credential_path):
        sys.stderr.write(
            f'Warning: GOOGLE_APPLICATION_CREDENTIALS file not found: {sa_credential_path}\n'
        )
        return None
    try:
        creds, _ = load_credentials_from_file(sa_credential_path, scopes=SCOPES)
        creds.refresh(Request())
        return creds.token
    except Exception as exc:
        sys.stderr.write(f'Warning: service account token refresh failed: {exc}\n')
        return None


def get_oauth_refresh_token_access_token():
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
    if not all([client_id, client_secret, refresh_token]):
        return None

    data = urllib.parse.urlencode(
        {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }
    ).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    try:
        with urllib.request.urlopen(req) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        sys.stderr.write(f'Warning: OAuth refresh failed with HTTP {exc.code}: {exc.read().decode()}\n')
        return None
    except urllib.error.URLError as exc:
        sys.stderr.write(f'Warning: OAuth refresh failed: {exc}\n')
        return None

    token = payload.get('access_token')
    if not token:
        sys.stderr.write('Warning: OAuth refresh response did not include access_token\n')
        return None
    return token


def get_access_token():
    token = get_service_account_token()
    if token:
        return token

    token = get_oauth_refresh_token_access_token()
    if token:
        return token

    token = os.getenv('GOOGLE_ACCESS_TOKEN')
    if token:
        return token

    sys.stderr.write(
        'Error: no authentication configured. Set GOOGLE_APPLICATION_CREDENTIALS, '
        'or GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET/GOOGLE_REFRESH_TOKEN, '
        'or GOOGLE_ACCESS_TOKEN.\n'
    )
    sys.exit(1)

def get_calendar_ids():
    # Support multiple IDs via env var (comma-separated) or single ID fallback.
    ids = os.getenv('GOOGLE_CALENDAR_IDS')
    if ids:
        return [c.strip() for c in ids.split(',') if c.strip()]
    # Fallback to single ID for backward compatibility.
    single = os.getenv('GOOGLE_CALENDAR_ID')
    return [single] if single else []

def request(method, url, data=None):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {get_access_token()}')
    req.add_header('Accept', 'application/json')
    if data:
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            # Handle 204 No Content for DELETE operations.
            if resp.getcode() == 204:
                return {}
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.stderr.write(f'HTTP error {e.code}: {e.read().decode()}\n')
        sys.exit(1)

def list_events(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='time_min', help='ISO start time')
    parser.add_argument('--to', dest='time_max', help='ISO end time')
    parser.add_argument('--max', dest='max_results', type=int, default=10)
    parsed = parser.parse_args(args)
    results = {}
    for cal_id in get_calendar_ids():
        params = {
            'maxResults': parsed.max_results,
            'singleEvents': 'true',
            'orderBy': 'startTime',
        }
        if parsed.time_min:
            params['timeMin'] = parsed.time_min
        if parsed.time_max:
            params['timeMax'] = parsed.time_max
        url = f"{BASE_URL}/calendars/{urllib.parse.quote(cal_id)}/events?{urllib.parse.urlencode(params)}"
        resp = request('GET', url)
        results[cal_id] = resp.get('items', [])
    print(json.dumps(results, indent=2))


def add_event(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', required=True)
    parser.add_argument('--start', required=True, help='ISO datetime')
    parser.add_argument('--end', required=True, help='ISO datetime')
    parser.add_argument('--desc', default='')
    parser.add_argument('--location', default='')
    parser.add_argument('--attendees', default='')
    parsed = parser.parse_args(args)
    cal_id = get_calendar_ids()[0] if get_calendar_ids() else None
    if not cal_id:
        sys.stderr.write('No calendar ID configured\n')
        sys.exit(1)
    event = {
        'summary': parsed.title,
        'start': {'dateTime': parsed.start},
        'end': {'dateTime': parsed.end},
        'description': parsed.desc,
        'location': parsed.location,
    }
    if parsed.attendees:
        event['attendees'] = [{'email': e.strip()} for e in parsed.attendees.split(',') if e.strip()]
    url = f"{BASE_URL}/calendars/{urllib.parse.quote(cal_id)}/events"
    data = json.dumps(event).encode()
    resp = request('POST', url, data=data)
    print(json.dumps(resp, indent=2))

def update_event(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--event-id', required=True)
    parser.add_argument('--title')
    parser.add_argument('--start')
    parser.add_argument('--end')
    parser.add_argument('--desc')
    parser.add_argument('--location')
    parser.add_argument('--attendees')
    parsed = parser.parse_args(args)
    cal_id = get_calendar_ids()[0] if get_calendar_ids() else None
    if not cal_id:
        sys.stderr.write('No calendar ID configured\n')
        sys.exit(1)
    get_url = f"{BASE_URL}/calendars/{urllib.parse.quote(cal_id)}/events/{urllib.parse.quote(parsed.event_id)}"
    event = request('GET', get_url)
    if parsed.title:
        event['summary'] = parsed.title
    if parsed.start:
        event.setdefault('start', {})['dateTime'] = parsed.start
    if parsed.end:
        event.setdefault('end', {})['dateTime'] = parsed.end
    if parsed.desc is not None:
        event['description'] = parsed.desc
    if parsed.location is not None:
        event['location'] = parsed.location
    if parsed.attendees:
        event['attendees'] = [{'email': e.strip()} for e in parsed.attendees.split(',') if e.strip()]
    resp = request('PUT', get_url, data=json.dumps(event).encode())
    print(json.dumps(resp, indent=2))

def delete_event(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--event-id', required=True)
    parsed = parser.parse_args(args)
    cal_id = get_calendar_ids()[0] if get_calendar_ids() else None
    if not cal_id:
        sys.stderr.write('No calendar ID configured\n')
        sys.exit(1)
    url = f"{BASE_URL}/calendars/{urllib.parse.quote(cal_id)}/events/{urllib.parse.quote(parsed.event_id)}"
    resp = request('DELETE', url)
    print(json.dumps(resp, indent=2))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: google_calendar.py <command> [options]\n')
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == 'list':
        list_events(args)
    elif cmd == 'add':
        add_event(args)
    elif cmd == 'update':
        update_event(args)
    elif cmd == 'delete':
        delete_event(args)
    else:
        sys.stderr.write(f'Unknown command: {cmd}\n')
        sys.exit(1)
