import streamlit as st
from src.db import get_posts, toggle_like, add_comment, get_comments
import time

def show_feed():
    st.header("📢 Community Feed")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_state = st.selectbox("Filter by State", ["All", "Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh", "Telangana", "Maharashtra", "Delhi", "Other"])
    with col2:
        filter_category = st.selectbox("Filter by Category", [
            "All",
            "Civic Sense & Public Responsibility",
            "Youth & Risk Behavior",
            "Women Safety & Social Issues",
            "Student Problems & Education",
            "Elder Care & Public Facilities",
            "Local Community Issues",
            "Awareness Articles"
        ])
    
    # Refresh logic
    if st.button("Refresh Feed"):
        st.rerun()
        
    posts = get_posts(category=filter_category, state=filter_state)
    
    if not posts:
        st.info("No posts found. Be the first to start a discussion!")
        return

    for post in posts:
        with st.container():
            st.markdown(f"### {post.get('title', 'Untitled')}")
            col_meta1, col_meta2 = st.columns([3, 1])
            with col_meta1:
                st.caption(f"📍 {post.get('region')}, {post.get('state')} | 🏷️ {post.get('category')}")
                st.caption(f"👤 {post.get('author_username')} | 🕒 {post.get('created_at')}")
            
            st.write(post.get('content'))
            
            if post.get('ai_summary'):
                st.info(f"🤖 **AI Summary:** {post.get('ai_summary')}")
            
            if post.get('hashtags'):
                st.write(f"**Tags:** {' '.join(post['hashtags'])}")

            # Interaction Bar
            col_int1, col_int2, col_int3 = st.columns(3)
            
            with col_int1:
                likes = post.get('likes_count', 0)
                if st.button(f"👍 Like ({likes})", key=f"like_{post['id']}"):
                    toggle_like(post['id'], st.session_state.user['localId'])
                    st.rerun()
            
            with col_int2:
                 st.write("💬 Comments")
            
            with col_int3:
                # Share Links
                share_text = f"Check out this post on Theru Kappom: {post.get('title')}"
                st.markdown(f"[Share on Twitter](https://twitter.com/intent/tweet?text={share_text})")

            # Comments Section
            with st.expander("View Comments"):
                comments = get_comments(post['id'])
                for c in comments:
                    st.text(f"{c.get('author_username')}: {c.get('text')}")
                
                new_comment = st.text_input("Add a comment...", key=f"comment_input_{post['id']}")
                if st.button("Post Comment", key=f"btn_comment_{post['id']}"):
                    if new_comment:
                        add_comment(post['id'], st.session_state.user['localId'], st.session_state.user.get('email').split('@')[0], new_comment)
                        st.success("Comment added!")
                        time.sleep(1)
                        st.rerun()

            st.divider()
