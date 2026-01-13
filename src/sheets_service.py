import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import config

def authenticate_sheets():
    """Authenticates specifically for Sheets API."""
    if os.path.exists(config.TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.SCOPES)
        return build('sheets', 'v4', credentials=creds)
    return None

def append_to_sheet(service, data):
    """
    Appends a list of values to the Google Sheet.
    data format: [['from', 'subject', 'date', 'content'], ...]
    """
    body = {
        'values': data
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=config.SPREADSHEET_ID,
        range=config.RANGE_NAME,
        valueInputOption='RAW', # Use RAW so Google doesn't format dates automatically
        body=body
    ).execute()
    
    print(f"{result.get('updates').get('updatedCells')} cells appended.")