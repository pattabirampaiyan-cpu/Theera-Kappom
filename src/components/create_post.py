import streamlit as st
from src.ai_helper import moderate_content, summarize_content, suggest_hashtags
from src.db import create_post
import time

def show_create_post():
    st.header("✍️ Speak Up for Change")
    st.caption("Share your thoughts on civic issues. Keep it constructive!")
    
    with st.form("create_post_form"):
        title = st.text_input("Title (e.g., Broken Street Lights in Anna Nagar)")
        category = st.selectbox("Category", [
            "Civic Sense & Public Responsibility",
            "Youth & Risk Behavior",
            "Women Safety & Social Issues",
            "Student Problems & Education",
            "Elder Care & Public Facilities",
            "Local Community Issues",
            "Awareness Articles"
        ])
        state = st.selectbox("State", ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana", "Maharashtra", "Delhi", "Other"])
        region = st.text_input("Region / City (e.g., Chennai)")
        content = st.text_area("Content", height=150, help="Describe the issue clearly.")
        uploaded_image = st.file_uploader("Attach Image (Optional)", type=["jpg", "png"])
        
        # Submit for Review First
        submitted = st.form_submit_button("Analyze & Preview")
    
    # Use session state to persist preview data
    if 'post_preview' not in st.session_state:
        st.session_state.post_preview = None

    if submitted:
        if not title or not content or not region:
            st.error("Please fill in all mandatory fields.")
        else:
            with st.spinner("AI is analyzing your content..."):
                is_safe, reason = moderate_content(f"{title} {content}")
                
            if not is_safe:
                st.error("⚠️ Content Flagged by AI")
                st.warning(f"Reason: {reason}")
                st.info("Please revise your post to adhere to community guidelines.")
            else:
                st.success("✅ Content looks good!")
                
                # Generate AI Extras
                summary = summarize_content(content)
                tags = suggest_hashtags(content)
                
                # Store in session state for the "Confirm" button to access
                st.session_state.post_preview = {
                    'title': title,
                    'content': content,
                    'category': category,
                    'state': state,
                    'region': region,
                    'summary': summary,
                    'tags': tags
                }

    # Show preview and confirm button if we have preview data
    if st.session_state.post_preview:
        preview = st.session_state.post_preview
        st.divider()
        st.subheader("Preview")
        st.write(f"**Title:** {preview['title']}")
        st.write(f"**Summary:** {preview['summary']}")
        st.write(f"**Hashtags:** {' '.join(preview['tags'])}")
        
        # Tags editing
        edited_tags = st.text_input("Edit Hashtags", value=" ".join(preview['tags']))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Confirm & Publish"):
                post_data = {
                    'author_uid': st.session_state.user['localId'],
                    'author_username': st.session_state.user.get('email', 'Anonymous').split('@')[0],
                    'title': preview['title'],
                    'content': preview['content'],
                    'category': preview['category'],
                    'hashtags': edited_tags.split(),
                    'state': preview['state'],
                    'region': preview['region'],
                    'ai_summary': preview['summary'],
                    'image_url': None
                }
                
                if create_post(post_data):
                    st.success("Post published successfully!")
                    st.session_state.post_preview = None # Clear after success
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to publish post. Try again.")
        with col2:
            if st.button("🗑️ Cancel"):
                st.session_state.post_preview = None
                st.rerun()
