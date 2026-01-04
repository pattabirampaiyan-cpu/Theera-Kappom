
import sys
import traceback

print("Checking imports...")

try:
    import streamlit
    print("Mask: streamlit [OK]")
except ImportError as e:
    print(f"Error: streamlit missing or failed: {e}")

try:
    import firebase_admin
    print("Mask: firebase-admin [OK]")
except ImportError as e:
    print(f"Error: firebase-admin missing or failed: {e}")

try:
    import google.generativeai
    print("Mask: google-generativeai [OK]")
except ImportError as e:
    print(f"Error: google-generativeai missing or failed: {e}")

try:
    import plotly
    print("Mask: plotly [OK]")
except ImportError as e:
    print(f"Error: plotly missing or failed: {e}")

try:
    import dotenv
    print("Mask: python-dotenv [OK]")
except ImportError as e:
    print(f"Error: python-dotenv missing or failed: {e}")

try:
    import streamlit_option_menu
    print("Mask: streamlit-option-menu [OK]")
except ImportError as e:
    print(f"Error: streamlit-option-menu missing or failed: {e}")

print("\nChecking local modules...")
try:
    import src.auth
    print("Mask: src.auth [OK]")
except Exception as e:
    print(f"Error: src.auth failed: {e}")
    traceback.print_exc()

try:
    import src.db
    print("Mask: src.db [OK]")
except Exception as e:
    print(f"Error: src.db failed: {e}")
    traceback.print_exc()

try:
    import src.components.feed
    print("Mask: src.components.feed [OK]")
except Exception as e:
    print(f"Error: src.components.feed failed: {e}")
    traceback.print_exc()

try:
    import src.components.create_post
    print("Mask: src.components.create_post [OK]")
except Exception as e:
    print(f"Error: src.components.create_post failed: {e}")
    traceback.print_exc()

try:
    import src.components.profile
    print("Mask: src.components.profile [OK]")
except Exception as e:
    print(f"Error: src.components.profile failed: {e}")
    traceback.print_exc()

try:
    import src.components.analytics
    print("Mask: src.components.analytics [OK]")
except Exception as e:
    print(f"Error: src.components.analytics failed: {e}")
    traceback.print_exc()

print("\nDone.")
