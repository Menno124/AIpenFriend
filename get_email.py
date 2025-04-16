from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json
from email import message_from_bytes

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_read_service():
    creds = None
    if os.path.exists('token_get_email.json'):
        creds = Credentials.from_authorized_user_file('token_get_email.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_get_email.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def load_allowed_emails(json_path='email_users.json'):
    with open(json_path, 'r') as f:
        users = json.load(f)
    return [user['email'].lower() for user in users]


def read_latest_emails(max_results=10):
    allowed_senders = load_allowed_emails()
    service = get_gmail_read_service()
    results = service.users().messages().list(userId='me', maxResults=max_results, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    print(f"📬 Checking {len(messages)} message(s) in the inbox:\n")

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()

        headers = msg_data['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(No sender)')
        snippet = msg_data.get('snippet', '')

        # Extract email address only (strip out "Name <email@domain>")
        if '<' in sender and '>' in sender:
            email_addr = sender.split('<')[1].split('>')[0].lower()
        else:
            email_addr = sender.lower()

        if email_addr in allowed_senders:
            print(f"✅ Matched Email From: {email_addr}")
            print(f"🔹 Subject: {subject}")
            print(f"   Snippet: {snippet}")
            print("-" * 60)

def get_matching_messages(max_results=10):
    allowed_senders = load_allowed_emails()
    service = get_gmail_read_service()
    results = service.users().messages().list(userId='me', maxResults=max_results, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    matching = []
    print(f"📬 Found {len(messages)} emails in inbox. Checking...\n")

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(No sender)')
        message_id = next((h['value'] for h in headers if h['name'] == 'Message-ID'), None)


        # Extract email
        if '<' in sender and '>' in sender:
            email_addr = sender.split('<')[1].split('>')[0].lower()
        else:
            email_addr = sender.lower()

        print(f"🧾 Found email from: {email_addr} | Subject: {subject}")

        if email_addr in allowed_senders:
            print(f"✅ Matched known sender: {email_addr}")
            matching.append({
                'email': email_addr,
                'subject': subject,
                'threadId': msg_data.get('threadId'),
                'messageId': msg['id'],
                'messageIdHeader': message_id
            })

        else:
            print(f"❌ Not in allowed senders list.")

    return matching




# 🧪 Example usage:
if __name__ == '__main__':
    read_latest_emails()
