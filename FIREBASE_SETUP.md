# 🔥 Firebase Setup Guide

## Step 1: Enable Firestore Database

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `resume-4036a`
3. Go to **Firestore Database** in the left sidebar
4. Click **Create database**
5. Choose **Start in test mode** (for development)
6. Select your preferred region
7. Click **Done**

## Step 2: Generate Service Account Key

1. In Firebase Console, go to **Project Settings** (gear icon)
2. Click on **Service accounts** tab
3. Click **Generate new private key**
4. Save the downloaded JSON file securely
5. Copy the contents and update `.streamlit/secrets.toml`

## Step 3: Update secrets.toml

Replace the placeholders in `.streamlit/secrets.toml` with values from your service account JSON:

```toml
[firebase_credentials]
type = "service_account"
project_id = "resume-4036a"
private_key_id = "YOUR_PRIVATE_KEY_ID_FROM_JSON"
private_key = "YOUR_PRIVATE_KEY_FROM_JSON"
client_email = "YOUR_CLIENT_EMAIL_FROM_JSON"
client_id = "YOUR_CLIENT_ID_FROM_JSON"
# ... other fields
```

## Step 4: For Streamlit Cloud Deployment

1. Go to your Streamlit Cloud app settings
2. Add all secrets from your local `.streamlit/secrets.toml`
3. Make sure the format matches exactly

## Step 5: Test the App

Run locally: `streamlit run stream.py`

The app should now work with Firebase authentication and database features!

## Security Notes

- ✅ Web config values (API keys, etc.) are safe to expose in client-side code
- 🔒 Service account private keys should NEVER be exposed publicly
- 🔒 Always use environment variables or secrets for server-side keys
- ✅ `.streamlit/secrets.toml` is already in `.gitignore`