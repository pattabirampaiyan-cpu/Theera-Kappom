import streamlit as st
from src.db import get_user_profile

def show_profile():
    st.header("👤 My Profile")
    
    user = st.session_state.user
    if not user:
        return
    
    # Fetch latest profile data
    profile = get_user_profile(user['localId'])
    
    if profile:
        col1, col2 = st.columns([1, 2])
        with col1:
             st.image("https://ui-avatars.com/api/?name=" + profile.get('username', 'User') + "&background=random", width=150)
        
        with col2:
            st.markdown(f"### {profile.get('username')}")
            st.write(f"**Email:** {profile.get('email')}")
            st.write(f"**State:** {profile.get('state')}")
            st.write(f"**Region:** {profile.get('region')}")
            st.write(f"**Role:** {profile.get('role', 'Public')}")
            
        st.divider()
        st.subheader("My Contributions")
        st.info("Feature coming soon: List of your created posts and comments.")
    else:
        st.error("Profile not found.")
