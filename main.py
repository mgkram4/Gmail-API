import os

from flask import Flask, redirect, render_template_string, request, session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Replace with your own Client ID and Client Secret
CLIENT_ID = ''
CLIENT_SECRET = ''
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

@app.route('/')
def index():
    return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    flow = Flow.from_client_config(
        {'web': {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'token_uri': 'https://oauth2.googleapis.com/token'}},
        scopes=SCOPES
    )
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_config(
        {'web': {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'token_uri': 'https://oauth2.googleapis.com/token'}},
        scopes=SCOPES
    )
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'
    flow.fetch_token(code=request.args.get('code'))
    session['credentials'] = flow.credentials.to_json()
    return redirect('/analyze_inbox')

def get_email_data(gmail_service, query, max_results=10):
    results = gmail_service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    messages = results.get('messages', [])
    email_data = []
    for message in messages:
        msg = gmail_service.users().messages().get(userId='me', id=message['id']).execute()
        snippet = msg['snippet']
        subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), 'No Subject')
        sentiment = TextBlob(snippet).sentiment.polarity
        email_data.append({
            'subject': subject,
            'snippet': snippet,
            'sentiment': sentiment
        })
    return email_data

@app.route('/analyze_inbox')
def analyze_inbox():
    if 'credentials' not in session:
        return redirect('/login')
    credentials = Credentials.from_authorized_user_info(eval(session['credentials']))
    gmail_service = build('gmail', 'v1', credentials=credentials)
    
    unread_emails = get_email_data(gmail_service, 'is:unread')
    recent_emails = get_email_data(gmail_service, '')
    
    return render_template_string('''
        <h1>Gmail Sentiment Analysis</h1>
        <h2>Unread Emails</h2>
        {% for email in unread_emails %}
            <div style="border: 1px solid #ddd; margin: 10px; padding: 10px;">
                <h3>{{ email.subject }}</h3>
                <p>{{ email.snippet }}</p>
                <p>Sentiment: {{ "%.2f"|format(email.sentiment) }}</p>
            </div>
        {% endfor %}
        <h2>Recent Emails</h2>
        {% for email in recent_emails %}
            <div style="border: 1px solid #ddd; margin: 10px; padding: 10px;">
                <h3>{{ email.subject }}</h3>
                <p>{{ email.snippet }}</p>
                <p>Sentiment: {{ "%.2f"|format(email.sentiment) }}</p>
            </div>
        {% endfor %}
    ''', unread_emails=unread_emails, recent_emails=recent_emails)

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # For development only
    app.run('localhost', 5000, debug=True)