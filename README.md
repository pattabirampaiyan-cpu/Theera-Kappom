# Theru Kappom – Makkal Kural

An AI-powered civic awareness and public voice platform.

## Setup Instructions

### 1. Environment Setup
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Firebase Configuration
You need a Firebase project with **Authentication** (Email/Password & Google) and **Firestore** enabled.

1. Go to [Firebase Console](https://console.firebase.google.com/).
2. Create a new project.
3. Enable **Authentication** (Email/Password provider).
4. Enable **Firestore Database** (Start in Test mode for development).
5. Go to **Project Settings > Service Accounts**.
6. Generate a new private key. This will download a JSON file.
7. Rename this file to `firebase-adminsdk.json` and place it in the root directory (DO NOT COMMIT THIS FILE).

### 3. Google Gemini AI Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Create a free API Key.
3. Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
   Or add it to `.streamlit/secrets.toml`:
   ```toml
   [general]
   GOOGLE_API_KEY = "your_api_key_here"
   ```

### 4. Run the Application
```bash
streamlit run main.py
```

## Features
- **Civic Awareness**: Share and discuss civic issues.
- **AI Integration**: Content moderation and summarization using Google Gemini.
- **Community**: Likes, comments, and sharing.
