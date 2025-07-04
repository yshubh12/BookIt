import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# If modifying these scopes, delete token.json
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_available_slots():
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow()
    end = now + timedelta(days=2)

    events_result = service.events().list(
        calendarId='primary', timeMin=now.isoformat() + 'Z', timeMax=end.isoformat() + 'Z',
        singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])
    booked = [e['start'].get('dateTime', '') for e in events]

    possible_slots = []
    for day in range(2):
        base = now + timedelta(days=day)
        for hour in range(9, 17):
            slot = base.replace(hour=hour, minute=0, second=0, microsecond=0)
            if slot.isoformat() + 'Z' not in booked and slot > now:
                readable = slot.strftime("%A, %B %d at %I:%M %p (UTC)")
                possible_slots.append({"iso": slot.isoformat(), "readable": readable})

    return possible_slots


def book_slot(start_time_iso):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    try:
        start_time = datetime.fromisoformat(start_time_iso)
        end_time = start_time + timedelta(minutes=30)

        event = {
            'summary': 'Booked via TailorTalk',
            'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'}
        }

        service.events().insert(calendarId='primary', body=event).execute()
        return True
    except Exception as e:
        print("Booking Error:", e)
        return False

def get_upcoming_appointments(limit=10):
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + timedelta(days=60)).isoformat() + 'Z'  # only next 2 months

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        maxResults=limit,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    readable_appointments = []

    for event in events:
        start = event['start'].get('dateTime')
        if start:
            dt = datetime.fromisoformat(start)
            readable = dt.strftime("%A, %B %d at %I:%M %p (UTC)")
            readable_appointments.append(f"{event['summary']} on {readable}")

    return readable_appointments
