# Gmail Sentiment Analysis App

This Flask application allows users to login with their Google account, analyze the sentiment of their unread emails, and display recent emails with their sentiment scores.

## Prerequisites

- Python 3.7+
- A Google Cloud project with Gmail API enabled
- OAuth 2.0 Client ID and Client Secret

## Setup

1. Clone this repository or create a new directory and save the provided code as `app.py`.

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

4. Install required packages:
   ```
   pip install flask google-auth google-auth-oauthlib google-api-python-client textblob
   ```

5. Set up Google Cloud:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API for your project
   - Create OAuth 2.0 credentials (Client ID and Client Secret)
   - Set up the OAuth consent screen and add your email as a test user

6. Configure the application:
   - Open `app.py` in a text editor
   - Replace the empty strings for `CLIENT_ID` and `CLIENT_SECRET` with your actual credentials:
     ```python
     CLIENT_ID = 'your_client_id_here'
     CLIENT_SECRET = 'your_client_secret_here'
     ```

## Running the Application

1. Ensure your virtual environment is activated.

2. Run the Flask application:
   ```
   python app.py
   ```

3. Open a web browser and go to `http://localhost:5000`

4. Click "Login with Google" and select your Google account (must be added as a test user).

5. If you see a warning that the app isn't verified, this is normal for development. Click "Advanced" and then "Go to [Your App Name] (unsafe)" to proceed.

6. The app will display your unread emails and recent emails with sentiment analysis.

## Important Notes

- This setup is for development and testing only. Do not use in production without proper security measures.
- The `OAUTHLIB_INSECURE_TRANSPORT` environment variable is set to '1' for local testing. Remove this in a production environment and use HTTPS.
- Keep your Client ID and Client Secret confidential. In a real-world scenario, these should be stored securely (e.g., environment variables) and not hardcoded in the script.

## Troubleshooting

- If you encounter a "redirect_uri_mismatch" error, ensure the redirect URI in your Google Cloud Console matches `http://localhost:5000/oauth2callback`.
- Clear your browser cache or use an incognito/private browsing window if you face persistent issues.
- Verify that you're using a Google account added as a test user in your Google Cloud project.

For any other issues, refer to the [Google OAuth 2.0 documentation](https://developers.google.com/identity/protocols/oauth2).
