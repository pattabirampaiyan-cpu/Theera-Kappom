import streamlit as st
import pyrebase
import os
from src.db import create_user_in_db, get_user_profile, initialize_firebase

def get_pyrebase_auth():
    try:
        # Use secrets if available, otherwise try env or fail gracefully
        # User snippet specifically asked for secrets mapping
        if "firebase" not in st.secrets:
            # Fallback for when secrets aren't set up yet? 
            # Or just let it fail so user knows to add them.
            return None

        firebase_config = {
            "apiKey": st.secrets["firebase"].get("apiKey", ""),
            "authDomain": st.secrets["firebase"].get("authDomain", ""),
            "projectId": st.secrets["firebase"].get("projectId", ""),
            "storageBucket": st.secrets["firebase"].get("storageBucket", ""),
            "messagingSenderId": st.secrets["firebase"].get("messagingSenderId", ""),
            "appId": st.secrets["firebase"].get("appId", ""),
            "databaseURL": "" # Required by pyrebase4 even if empty
        }
        
        firebase = pyrebase.initialize_app(firebase_config)
        return firebase.auth()
    except Exception as e:
        # Silent fail or log? Better to let user know config is wrong if they try to login
        # We'll handle exceptions in login/signup
        raise e

def login_user(email, password):
    try:
        auth = get_pyrebase_auth()
        if not auth:
            st.error("Firebase Configuration missing in secrets.")
            return None
            
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        # Parse error message for better UI
        error_msg = str(e)
        if "INVALID_PASSWORD" in error_msg:
            st.error("Incorrect password.")
        elif "EMAIL_NOT_FOUND" in error_msg:
            st.error("Email not found.")
        else:
            st.error(f"Login failed: {e}")
        return None

def signup_user(email, password):
    try:
        auth = get_pyrebase_auth()
        if not auth:
            st.error("Firebase Configuration missing in secrets.")
            return None
            
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        error_msg = str(e)
        if "EMAIL_EXISTS" in error_msg:
             st.error("Email already exists.")
        else:
            st.error(f"Signup Error: {e}")
        return None

def init_session():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = None
    
    # Ensure Firebase Admin is initialized (for Firestore)
    initialize_firebase()
