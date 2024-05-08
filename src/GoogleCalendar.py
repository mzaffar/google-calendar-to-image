import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendar:
    def __init__(self):
        print("GoogleCalendar")
        self.SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
        self.creds = None
        self.service = None
        self.get_creds()

    def get_creds(self):
        print("Getting credentials")
        if os.path.exists("credentials/token.json"):
            self.creds = Credentials.from_authorized_user_file("credentials/token.json", self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials/credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open("credentials/token.json", "w") as token:
                token.write(self.creds.to_json())  

        self.service = build("calendar", "v3", credentials=self.creds)


    def export_to_json(self):
        print("Getting calendar data")

        # get first day of the month
        first_day_of_month = datetime.datetime.now().replace(day=1)

        # get last day of the month
        last_day_of_month = datetime.datetime.now().replace(day=1, month=first_day_of_month.month+1) - datetime.timedelta(days=1)

        # Get calendar
        calendars_result = self.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        items = []
        for calendar in calendars:
            id = calendar['id']
            backgroundColor = calendar.get('backgroundColor', '#ffffff')
            foregroundColor = '#ffffff'#calendar.get('foregroundColor', '#ffffff')

            events_result = (
                self.service.events()
                .list(
                    calendarId=id,
                    timeMin=first_day_of_month.isoformat() + "Z",
                    timeMax=last_day_of_month.isoformat() + "Z",
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])

            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))

                item = {
                    'start': event["start"],
                    'day': start.split('T')[0].split('-')[2],
                    'end': event["end"],
                    'summary': event["summary"],
                    'backgroundColor': backgroundColor,
                    'foregroundColor': foregroundColor,
                }
                items.append(item)

        with open('events.json', 'w') as file:
            json.dump(items, file, indent=4)


        