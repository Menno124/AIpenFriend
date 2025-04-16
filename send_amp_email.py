import os
import base64
import pickle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # THIS OPENS YOUR BROWSER
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def create_amp_email(to_email):
    message = MIMEMultipart('alternative')
    message['To'] = to_email
    message['From'] = "me"
    message['Subject'] = "🎉 Your First Interactive PenFriend Mail"

    plain_text = "This is the plain text fallback."

    html_text = """
    <html>
      <body>
        <p>This is the <b>HTML fallback</b> version.</p>
      </body>
    </html>
    """

    amp_html = """
    <!doctype html>
    <html ⚡4email>
    <head>
      <meta charset="utf-8">
      <script async src="https://cdn.ampproject.org/v0.js"></script>
      <script async custom-element="amp-form"
        src="https://cdn.ampproject.org/v0/amp-form-0.1.js"></script>
      <style amp4email-boilerplate>body{visibility:hidden}</style>
      <style amp-custom>
        h1 { color: #007BFF; }
        button { background: #28a745; color: white; padding: 10px; border: none; }
      </style>
    </head>
    <body>
      <h1>Hello from PenFriend 🤖</h1>
      <p>Want to keep chatting?</p>
      <form method="POST" action-xhr="https://example.com/reply" target="_blank">
        <input type="hidden" name="user_id" value="1234">
        <button type="submit" name="reply" value="yes">Yes 😊</button>
        <button type="submit" name="reply" value="no">No 👋</button>
      </form>
    </body>
    </html>
    """

    message.attach(MIMEText(plain_text, 'plain'))
    message.attach(MIMEText(html_text, 'html'))
    message.attach(MIMEText(amp_html, 'x-amp-html'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(service, message):
    try:
        sent_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"✅ Email sent! Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # 👇 Replace this with your Gmail address to test
    your_email = "aipenfriendru@gmail.com"
    service = authenticate_gmail()
    msg = create_amp_email(your_email)
    send_email(service, msg)
