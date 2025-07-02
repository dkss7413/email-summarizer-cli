import os
import pickle
from typing import List, Dict
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from pathlib import Path
from bs4 import BeautifulSoup
import re
import email
from email import policy
from email.parser import BytesParser

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
PROJECT_ROOT = Path(__file__).parent.parent
TOKEN_PATH = str(PROJECT_ROOT / "token.pickle")
CREDENTIALS_PATH = str(PROJECT_ROOT / "credentials.json")

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_recent_emails(max_results=10) -> List[Dict]:
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=max_results, q='category:primary').execute()
    messages = results.get('messages', [])
    email_list = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From','Subject','Date']).execute()
        headers = {h['name']: h['value'] for h in msg_detail['payload']['headers']}
        email_list.append({
            'id': msg['id'],
            'from': headers.get('From', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', '')
        })
    return email_list

def extract_text_from_email(raw_email):
    # 표준 라이브러리 email로 robust하게 파싱
    msg = BytesParser(policy=policy.default).parsebytes(raw_email.encode('utf-8', errors='replace'))
    text_plain = []
    text_html = []
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content = part.get_payload(decode=True)
            if content_type == 'text/plain' and content:
                text_plain.append(content.decode(part.get_content_charset() or 'utf-8', errors='replace'))
            elif content_type == 'text/html' and content:
                text_html.append(content.decode(part.get_content_charset() or 'utf-8', errors='replace'))
    else:
        content_type = msg.get_content_type()
        content = msg.get_payload(decode=True)
        if content_type == 'text/plain' and content:
            text_plain.append(content.decode(msg.get_content_charset() or 'utf-8', errors='replace'))
        elif content_type == 'text/html' and content:
            text_html.append(content.decode(msg.get_content_charset() or 'utf-8', errors='replace'))
    if text_plain:
        return '\n'.join(text_plain)
    elif text_html:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup('\n'.join(text_html), 'html.parser')
        return soup.get_text(separator='\n', strip=True)
    else:
        return ''

def get_email_body(message_id: str) -> str:
    service = get_gmail_service()
    try:
        msg = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
        import base64
        raw_data = base64.urlsafe_b64decode(msg['raw'].encode('ASCII')).decode('utf-8', errors='replace')
        return extract_text_from_email(raw_data)
    except Exception:
        return '' 