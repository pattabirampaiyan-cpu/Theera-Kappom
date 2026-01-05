import streamlit as st
from src.auth import init_session, login_user, signup_user
from src.db import create_user_in_db, get_user_profile, update_onboarding_status
from streamlit_option_menu import option_menu

# Page Config
st.set_page_config(
    page_title="Theru Kappom – Makkal Kural",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session
init_session()

def main():
    if not st.session_state.user:
        login_page()
    else:
        # Check Onboarding
        user_profile = get_user_profile(st.session_state.user['localId'])
        if not user_profile:
             # Just in case details aren't in Firestore yet (rare sync issue or first run)
             st.warning("Profile not found. Please complete setup.")
             onboarding_page()
        elif not user_profile.get('onboarding_completed', False):
            onboarding_page()
        else:
            main_app_layout()

def login_page():
    st.title("📢 Theru Kappom – Makkal Kural")
    st.subheader("Civic Awareness & Public Voice Platform")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Login failed. Check credentials or API Key.")

    with tab2:
        new_email = st.text_input("Email", key="full_email")
        new_pass = st.text_input("Password", type="password", key="full_pass")
        new_username = st.text_input("Username")
        pk_state = st.selectbox("State", ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana", "Maharashtra", "Delhi", "Other"])
        pk_region = st.text_input("City / District")
        pk_age = st.selectbox("Age Group", ["<18", "18-25", "26-40", "40+"])
        
        if st.button("Sign Up"):
            if not new_username or not pk_region:
                st.error("Please fill all fields.")
            else:
                user = signup_user(new_email, new_pass)
                if user:
                    # Create Firestore Profile
                    create_user_in_db(user['localId'], new_email, new_username, pk_state, pk_region, pk_age)
                    
                    # Auto-login (simulate or ask to login)
                    st.success("Account created! Please login.")
                else:
                    st.error("Signup failed.")

def onboarding_page():
    st.title("Welcome to Theru Kappom! 🌟")
    st.info("Before you start, please review our community guidelines.")
    
    st.markdown("""
    ### 🛡️ Community Guidelines
    1. **Civic Issues Only**: Focus on public responsibility, safety, and infrastructure.
    2. **No Personal Attacks**: Do not name or shame individuals. Use generic terms like 'local authority' or 'admin'.
    3. **Constructive Dialogue**: Suggest solutions, don't just complain.
    4. **Be Respectful**: Hate speech and abusive language are strictly prohibited.
    
    ### 📝 How it works
    - **Post**: Share your story or observation.
    - **AI Check**: Our AI ensures safe and clean content.
    - **Discuss**: Engage with others to find solutions.
    """)
    
    if st.button("I Agree & Continue"):
        if st.session_state.user:
            update_onboarding_status(st.session_state.user['localId'])
            st.rerun()

def main_app_layout():
    with st.sidebar:
        st.write(f"Welcome, **{st.session_state.user.get('email')}**")
        
        selected = option_menu(
            "Menu", ["Feed", "Create Post", "Profile", "Statistics"],
            icons=["house", "pencil-square", "person", "graph-up"],
            menu_icon="cast", default_index=0
        )
        
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

    if selected == "Feed":
        from src.components.feed import show_feed
        show_feed()
    elif selected == "Create Post":
        from src.components.create_post import show_create_post
        show_create_post()
    elif selected == "Profile":
        from src.components.profile import show_profile
        show_profile()
    elif selected == "Statistics":
        from src.components.analytics import show_analytics
        show_analytics()

if __name__ == "__main__":
    main()
