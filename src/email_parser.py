import base64
from bs4 import BeautifulSoup

def clean_body(data):
    """
    Decodes base64url and strips HTML tags to satisfy the 'plain text' requirement.
    """
    if not data:
        return ""
    # Decode Base64
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_str = decoded_bytes.decode('utf-8')
    
    # Strip HTML using BeautifulSoup (Bonus feature & Cleaner data)
    soup = BeautifulSoup(decoded_str, "html.parser")
    return soup.get_text(separator=' ', strip=True)

def parse_email(message):
    """
    Parses the raw Gmail API message object into a simple dictionary.
    """
    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    
    # 1. Extract Headers
    email_data = {
        "id": message.get("id"),
        "From": "Unknown",
        "Subject": "(No Subject)",
        "Date": "Unknown",
        "Content": ""
    }
    
    for header in headers:
        name = header.get('name')
        value = header.get('value')
        if name == 'From':
            email_data['From'] = value
        elif name == 'Subject':
            email_data['Subject'] = value
        elif name == 'Date':
            email_data['Date'] = value

    # 2. Extract Body (Handles Multipart vs Singlepart)
    # The API structure varies if the email has attachments/HTML
    body_data = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                body_data = part['body'].get('data', '')
                break  # Prefer plain text
            elif part['mimeType'] == 'text/html':
                body_data = part['body'].get('data', '') # Fallback to HTML
    else:
        # Simple email
        body_data = payload.get('body', {}).get('data', '')

    email_data['Content'] = clean_body(body_data)
    
    return email_data