from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import base64
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


def read_latest_emails(max_results=3):
    service = get_gmail_read_service()
    results = service.users().messages().list(userId='me', maxResults=max_results, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    print(f"📬 Found {len(messages)} message(s) in the inbox:\n")

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()

        headers = msg_data['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(No sender)')
        snippet = msg_data.get('snippet', '')

        print(f"🔹 Subject: {subject}")
        print(f"   From: {sender}")
        print(f"   Snippet: {snippet}")
        print("-" * 60)


# 🧪 Example usage:
if __name__ == '__main__':
    read_latest_emails()
