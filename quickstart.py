import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the names and start times of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0, open_browser=False)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

        # Refer to the Python quickstart on how to setup the environment.
    # https://developers.google.com/calendar/api/quickstart/python
    event = {
        "summary": "Prueba de API",
        "location": "Google Meet",
        "description": "Un evento de prueba creado automáticamente desde nuestro script de Python.",
        "start": {
            "dateTime": "2025-08-19T09:00:00-05:00",
            "timeZone": "America/Bogota",
        },
        "end": {
            "dateTime": "2025-08-19T10:00:00-05:00",
            "timeZone": "America/Bogota",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Evento creado: {event.get('htmlLink')}")

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()