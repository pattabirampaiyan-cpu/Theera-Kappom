import streamlit as st
import firebase_admin
from firebase_admin import auth as admin_auth
from src.db import create_user_in_db, get_user_profile, initialize_firebase

def login_user(email, password):
    # Note: Firebase Admin SDK does NOT support Client-side Email/Password Login (verifyPassword).
    # It is a specialized SDK for server-side management.
    # For a Streamlit-only managed solution without a frontend JS SDK, we would typically use the Identity Toolkit API REST endpoint.
    # However, to keep it "Code Only" and robust, we will simulate the flow or requires the user's WEB API KEY.
    # Using a helper for REST API login if key is available.
    
    # For this implementation foundation, we will rely on a mock successful login if we can't hit the real endpoint 
    # OR we implement the REST call which is the standard way for python clients.
    
    # We need the Web API Key for this.
    try:
        # To make this real, we need the API KEY. I'll prompt for it in UI if missing, or use a placeholder.
        # Ideally, we use pyrebase4 or requests.
        import requests
        import json
        
        web_api_key = st.secrets.get("firebase", {}).get("web_api_key") or os.environ.get("FIREBASE_WEB_API_KEY")
        if not web_api_key:
            st.error("Missing Firebase Web API Key for Authentication. Please add it to secrets/env.")
            return None

        request_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={web_api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"email": email, "password": password, "returnSecureToken": True}
        
        response = requests.post(request_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json() # Contains localId (uid), idToken, etc.
        
    except Exception as e:
        # st.error(f"Login failed: {e}") # Let the UI handle error display
        return None

def signup_user(email, password):
    try:
        # Create user in Firebase Auth
        user = admin_auth.create_user(
            email=email,
            password=password
        )
        return user
    except Exception as e:
        st.error(f"Signup Error: {e}")
        return None

def init_session():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = None
    
    # Ensure Firebase is initialized
    initialize_firebase()

import os
