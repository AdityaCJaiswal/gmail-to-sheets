import os
import json
import config
import gmail_service
import sheets_service
import email_parser

def load_state():
    """
    Loads the list of processed email IDs from state.json.
    This fulfills the requirement: 'Store and reuse state'[cite: 52].
    """
    if os.path.exists(config.STATE_FILE):
        try:
            with open(config.STATE_FILE, 'r') as f:
                return set(json.load(f)) # Use a set for O(1) lookups
        except json.JSONDecodeError:
            return set()
    return set()

def save_state(processed_ids):
    """
    Saves the updated list of processed email IDs.
    """
    with open(config.STATE_FILE, 'w') as f:
        # Convert set back to list for JSON serialization
        json.dump(list(processed_ids), f)

def main():
    print("--- Starting Gmail to Sheets Automation ---")
    
    # 1. Authenticate Services
    gmail = gmail_service.authenticate_gmail()
    sheets = sheets_service.authenticate_sheets()
    
    # 2. Load State (Duplicate Prevention)
    processed_ids = load_state()
    print(f"Loaded {len(processed_ids)} previously processed IDs.")
    
    # 3. Fetch Unread Emails
    # We fetch unread emails as per requirement [cite: 31, 49]
    messages = gmail_service.fetch_unread_emails(gmail)
    
    if not messages:
        print("No unread emails found.")
        return

    new_rows = []
    new_ids = []

    print(f"Found {len(messages)} unread emails. Processing...")

    for msg in messages:
        msg_id = msg['id']
        
        # DUPLICATE CHECK: If we've seen this ID before, skip it.
        # This fulfills 'No duplicate rows allowed' [cite: 26]
        if msg_id in processed_ids:
            print(f"Skipping duplicate email ID: {msg_id}")
            continue
            
        # 4. Parse Email
        full_msg = gmail_service.get_message_details(gmail, msg_id)
        email_data = email_parser.parse_email(full_msg)
        
        # Prepare row for Sheets: [From, Subject, Date, Content]
        row = [
            email_data['From'],
            email_data['Subject'],
            email_data['Date'],
            email_data['Content']
        ]
        new_rows.append(row)
        new_ids.append(msg_id)

    # 5. Append to Google Sheets
    if new_rows:
        print(f"Appending {len(new_rows)} rows to Sheets...")
        sheets_service.append_to_sheet(sheets, new_rows)
        
        # 6. Mark as Read & Update State
        # Only mark read AFTER successful write to sheets to ensure data safety
        gmail_service.mark_as_read(gmail, new_ids)
        
        processed_ids.update(new_ids)
        save_state(processed_ids)
        print("Success! State updated.")
    else:
        print("No new unique emails to process.")

if __name__ == '__main__':
    main()