import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

# Initialize Firebase (Singleton pattern)
def initialize_firebase():
    if not firebase_admin._apps:
        # Check for service account key
        cred_path = "firebase-adminsdk.json"
        
        # Try to find credentials either in file or streamlit secrets
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
        elif "firebase" in st.secrets:
             # Construct certificate from secrets if available
            cred_info = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_info)
        else:
            return None # Indicate missing credentials
            
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

def get_db():
    try:
        return initialize_firebase()
    except Exception as e:
        st.error(f"Failed to connect to Database: {e}")
        return None

# --- User Operations ---
def create_user_in_db(uid, email, username, state, region, age_group):
    db = get_db()
    if not db: return False
    
    user_ref = db.collection('users').document(uid)
    user_data = {
        'uid': uid,
        'email': email,
        'username': username,
        'state': state,
        'region': region,
        'age_group': age_group,
        'role': 'public', # Default role
        'onboarding_completed': False,
        'created_at': firestore.SERVER_TIMESTAMP
    }
    user_ref.set(user_data)
    return True

def get_user_profile(uid):
    db = get_db()
    if not db: return None
    
    doc = db.collection('users').document(uid).get()
    if doc.exists:
        return doc.to_dict()
    return None

def update_onboarding_status(uid):
    db = get_db()
    if not db: return
    
    db.collection('users').document(uid).update({
        'onboarding_completed': True
    })

# --- Post Operations ---
def create_post(post_data):
    db = get_db()
    if not db: return False
    
    # Add timestamp server-side
    post_data['created_at'] = firestore.SERVER_TIMESTAMP
    post_data['likes_count'] = 0
    
    db.collection('posts').add(post_data)
    return True

def get_posts(category=None, state=None, limit=20):
    db = get_db()
    if not db: return []
    
    posts_ref = db.collection('posts')
    query = posts_ref.order_by('created_at', direction=firestore.Query.DESCENDING)
    
    if category and category != "All":
        query = query.where('category', '==', category)
    
    if state and state != "All":
        query = query.where('state', '==', state)
        
    docs = query.limit(limit).stream()
    return [doc.to_dict() | {'id': doc.id} for doc in docs]

# --- Interaction Operations ---
def toggle_like(post_id, user_uid):
    db = get_db()
    if not db: return
    
    # Use a subcollection or separate collection for likes to prevent duplicate likes
    # Simplified handling: Check if like exists
    like_ref = db.collection('posts').document(post_id).collection('likes').document(user_uid)
    post_ref = db.collection('posts').document(post_id)
    
    if like_ref.get().exists:
        # Unlike
        like_ref.delete()
        post_ref.update({'likes_count': firestore.Increment(-1)})
    else:
        # Like
        like_ref.set({'timestamp': firestore.SERVER_TIMESTAMP})
        post_ref.update({'likes_count': firestore.Increment(1)})

def add_comment(post_id, user_uid, username, text):
    db = get_db()
    if not db: return
    
    comment_data = {
        'post_id': post_id,
        'author_uid': user_uid,
        'author_username': username,
        'text': text,
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    # Store in subcollection
    db.collection('posts').document(post_id).collection('comments').add(comment_data)
    
def get_comments(post_id):
    db = get_db()
    if not db: return []
    
    docs = db.collection('posts').document(post_id).collection('comments').order_by('created_at').stream()
    return [doc.to_dict() for doc in docs]
