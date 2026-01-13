import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import config

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(config.TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.CREDENTIALS_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(config.TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

if __name__ == '__main__':
    print("Attempting to authenticate...")
    service = authenticate_gmail()
    print("Authentication successful! Service created.")

    # ... (Keep your imports and authenticate_gmail function) ...

def fetch_unread_emails(service):
    """
    Fetches a list of unread email messages (IDs and ThreadIDs).
    """
    # query 'is:unread' matches the assignment requirement
    # Modified query to fetch ONLY unread emails with a specific subject
# This fulfills the "Bonus: Subject-based filtering" requirement
    query = 'is:unread subject:"LeetCode Weekly Digest"' 
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_message_details(service, msg_id):
    """
    Fetches the full payload of a specific email ID.
    """
    return service.users().messages().get(userId='me', id=msg_id, format='full').execute()

def mark_as_read(service, msg_ids):
    """
    Batch modifies emails to remove the 'UNREAD' label.
    """
    if not msg_ids:
        return
        
    service.users().messages().batchModify(
        userId='me',
        body={
            'ids': msg_ids,
            'removeLabelIds': ['UNREAD']
        }
    ).execute()
    print(f"Marked {len(msg_ids)} emails as read.")