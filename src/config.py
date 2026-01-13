import os

# usage: src/config.py

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials', 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'credentials', 'token.json')
STATE_FILE = os.path.join(BASE_DIR, 'state.json')

# Google API Scopes
# distinct scopes for Gmail (Read/Modify) and Sheets (Write)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',  # Needed to remove UNREAD label [cite: 32]
    'https://www.googleapis.com/auth/spreadsheets'   # Needed to write to sheets [cite: 23]
]

# Spreadsheet Config
SPREADSHEET_ID = '1GGo_5SiFVpTNIjGxa-iNNA3n8kgLg7yJ_9_-KnTCNcA' 
RANGE_NAME = 'Sheet1!A:D' # Appends to columns A-D