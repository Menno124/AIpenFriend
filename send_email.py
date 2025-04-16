import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def create_amp_email(to_email):
    message = MIMEMultipart('alternative')
    message['To'] = to_email
    message['From'] = "aipenfriendru@gmail.com"  # ✅ Use your actual Gmail here
    message['Subject'] = "📬 Explore PenFriend Mail (AMP)"

    plain_text = "This is a fallback for mail clients that do not support HTML or AMP."

    html_text = """
    <html>
      <body>
        <p>This is the <b>HTML fallback</b> version of the interactive AMP email.</p>
        <p>To experience the full interactive version, open this mail in Gmail Web.</p>
      </body>
    </html>
    """

    amp_html = """<!doctype html>
<html ⚡4email data-css-strict>
  <head>
    <meta charset="utf-8">
    <script async src="https://cdn.ampproject.org/v0.js"></script>
    <script async custom-element="amp-bind" src="https://cdn.ampproject.org/v0/amp-bind-0.1.js"></script>
    <script async custom-element="amp-selector" src="https://cdn.ampproject.org/v0/amp-selector-0.1.js"></script>
    <style amp4email-boilerplate>body{visibility:hidden}</style>
    <style amp-custom>
      body {
        font-family: Arial, sans-serif;
        background: #f4f4f4;
        padding: 20px;
        color: #333;
      }
      .button {
        margin: 5px;
        padding: 10px 16px;
        background: #4caf50;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
      }
      .page {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        margin-top: 10px;
      }
    </style>
  </head>
  <body>
    <amp-state id="view">
      <script type="application/json">
        { "page": "home" }
      </script>
    </amp-state>
    <div>
      <button class="button" on="tap:AMP.setState({ view: { page: 'home' } })">Home</button>
      <button class="button" on="tap:AMP.setState({ view: { page: 'shop' } })">Shop</button>
      <button class="button" on="tap:AMP.setState({ view: { page: 'profile' } })">Profile</button>
      <button class="button" on="tap:AMP.setState({ view: { page: 'settings' } })">Settings</button>
    </div>
    <div class="page" [hidden]="view.page != 'home'">
      <h2>Home Page</h2>
      <p>This is the home view for the AI Pen-Friend letters.</p>
    </div>
    <div class="page" hidden [hidden]="view.page != 'shop'">
      <h2>PenFriend Shop</h2>
      <p>Browse and filter pen-friends.</p>
    </div>
    <div class="page" hidden [hidden]="view.page != 'profile'">
      <h2>PenFriend Profile</h2>
      <p>Details about a selected pen-friend.</p>
    </div>
    <div class="page" hidden [hidden]="view.page != 'settings'">
      <h2>Settings</h2>
      <p>Manage your preferences and topics.</p>
    </div>
  </body>
</html>"""

    message.attach(MIMEText(plain_text, 'plain'))
    message.attach(MIMEText(html_text, 'html'))
    message.attach(MIMEText(amp_html, 'x-amp-html'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}




def send_amp_email(to_email):
    service = get_gmail_service()
    email_body = create_amp_email(to_email)

    try:
        sent = service.users().messages().send(userId='me', body=email_body).execute()
        print(f"✅ AMP email sent! Message ID: {sent['id']}")
        return sent
    except Exception as e:
        print(f"❌ Failed to send AMP email: {e}")
        return None


# 🧪 Example usage:
if __name__ == '__main__':
    send_amp_email('hahurymenno95@gmail.com')
