import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from createStudentJson import studentJson
from createFormResponsesJson import formResponses
from createPossibleHours import possibleHours
from calculatePossibleHours import PossibleHoursBetween
from calculateStudentHours import studentHoursBetween
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def main():
    studentJson()
    formResponses()
    possibleHours()
    print(PossibleHoursBetween("09/08/2023", "09/11/2023"))
    print(studentHoursBetween( "171821","09/09/2023", "09/09/2023"))
if __name__ == "__main__":
  main()