import google.generativeai as genai
import streamlit as st
import os

def configure_genai():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key and "general" in st.secrets:
        api_key = st.secrets["general"].get("GOOGLE_API_KEY")
    
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def moderate_content(text):
    """
    Checks if the content is safe.
    Returns: (is_safe: bool, reason: str)
    """
    if not configure_genai():
        return True, "AI Moderation unavailable (Key missing). Allowing provisionally."

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a moderation AI for a civic awareness platform.
    Analyze the following text for hate speech, abusive language, personal attacks, or incitement to violence.
    Also ensure it is NOT a specific personal complaint against an individual (naming/shaming) but rather a general civic issue.
    
    Text: "{text}"
    
    Output strictly in this format:
    SAFE: [Yes/No]
    REASON: [Brief explanation if No, otherwise None]
    """
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        is_safe = "SAFE: Yes" in result
        
        reason = "Content violates guidelines."
        for line in result.split('\n'):
            if line.startswith("REASON:"):
                reason = line.replace("REASON:", "").strip()
        
        return is_safe, reason
    except Exception as e:
        return True, f"AI Error: {e}. Allowing provisionally."

def summarize_content(text):
    if not configure_genai():
        return text[:100] + "..."

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Summarize this civic issue in 1-2 sentences, highlighting the key problem and location if mentioned: {text}"
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return text[:100] + "..."

def suggest_hashtags(text):
    if not configure_genai():
        return []

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Suggest 3-5 relevant, short hashtags for this content (Output format: #Tag1 #Tag2 ...): {text}"
    
    try:
        response = model.generate_content(prompt)
        tags = [t for t in response.text.strip().split() if t.startswith('#')]
        return tags
    except:
        return []
