import streamlit as st
import pandas as pd
import plotly.express as px
from src.db import get_posts

def show_analytics():
    st.header("📊 Civic Insights")
    st.caption("Anonymous aggregated data on community issues.")
    
    # Fetch all posts (for demo purpose; in prod, use aggregation queries)
    posts = get_posts(limit=100)
    
    if not posts:
        st.info("Not enough data to generate insights yet.")
        return

    df = pd.DataFrame(posts)
    
    # 1. Issues by Category
    st.subheader("Top Issues by Category")
    if 'category' in df.columns:
        cat_counts = df['category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        fig_cat = px.bar(cat_counts, x='Category', y='Count', color='Category', title="Issues Reported per Category")
        st.plotly_chart(fig_cat, use_container_width=True)
    
    # 2. Issues by State
    st.subheader("Activity by State")
    if 'state' in df.columns:
        state_counts = df['state'].value_counts().reset_index()
        state_counts.columns = ['State', 'Count']
        fig_state = px.pie(state_counts, values='Count', names='State', title="Distribution by State")
        st.plotly_chart(fig_state, use_container_width=True)

    # 3. Trending Hashtags
    st.subheader("Trending Hashtags")
    all_tags = []
    if 'hashtags' in df.columns:
        for tags in df['hashtags'].dropna():
            if isinstance(tags, list):
                all_tags.extend(tags)
    
    if all_tags:
        tag_series = pd.Series(all_tags).value_counts().head(10).reset_index()
        tag_series.columns = ['Hashtag', 'Mentions']
        fig_tags = px.bar(tag_series, x='Mentions', y='Hashtag', orientation='h', title="Top 10 Trending Topics")
        st.plotly_chart(fig_tags, use_container_width=True)
