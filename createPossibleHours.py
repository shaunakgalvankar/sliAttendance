import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1loZQ2-2HxIksYoqVMLnolQQJpXI4io-Cdn6JYap6zcQ"
SAMPLE_RANGE_NAME = "possibleHours"


def possibleHours():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Call the Sheets API
    service = build('sheets', 'v4', credentials=creds)

    # Fetch the data from the spreadsheet
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    # Create a dictionary to store the data
    data = {}
    for row in values[2:]:  # Skip the first two rows (header rows)
        if len(row) >= 3:
            date_str = row[2]
            date = datetime.datetime.strptime(date_str, "%B %d %Y")  # Parse date in month date year format
            day_of_week = date.strftime("%A")
            time = row[3]
            data[date.strftime("%m/%d/%Y")] = [day_of_week, time]  # Format date as "mm/dd/yyyy"

    # Write the data to a JSON file with indentation
    with open('possibleHours.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
