import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import json
from datetime import datetime
from dateutil import parser

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1loZQ2-2HxIksYoqVMLnolQQJpXI4io-Cdn6JYap6zcQ"
SAMPLE_RANGE_NAME = "Form Responses 1"

def formResponses():
    # Load credentials from token.json if available, otherwise prompt the user to authorize the application
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the service object
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    # Create a dictionary to store the data
    data = {}
    for i, row in enumerate(values):
        if i == 0:  # Skip the first row
            continue
        if len(row) > 2:  # Check if row has enough elements
            student_id = row[2]
            date = row[0]
            day_of_week=datetime.strptime(date, "%m/%d/%Y %H:%M:%S").strftime("%A")
            columns = [row[0], row[1], day_of_week]
            if student_id not in data:
                data[student_id] = []
            data[student_id].append(columns)

    # Write the JSON object to a file with indentation for better readability
    with open('responses.json', 'w') as file:
        json.dump(data, file, indent=4)


formResponses()