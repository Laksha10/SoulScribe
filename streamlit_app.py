import streamlit as st
import requests
# import psycopg2
# from urllib.parse import urlparse
# from datetime import datetime
# import os
# from dotenv import load_dotenv

# --- Load Environment Variables ---
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")

# Parse connection info
# parsed_url = urlparse(DATABASE_URL)
# DB_USER = parsed_url.username
# DB_PASSWORD = parsed_url.password
# DB_HOST = parsed_url.hostname
# DB_PORT = parsed_url.port
# DB_NAME = parsed_url.path[1:]

# --- Streamlit Page Setup ---
st.set_page_config(page_title="SoulScribe", page_icon="🕊️", layout="centered")

# --- Custom CSS for readable layout ---
st.markdown("""
    <style>
        .stApp {
            background-color: #f9fafb;
            color: #111827;
            font-family: 'Segoe UI', sans-serif;
        }
        textarea {
            background-color: #ffffff !important;
            color: #111827 !important;
            font-size: 16px !important;
            border-radius: 10px !important;
            padding: 10px !important;
            border: 1px solid #d1d5db !important;
        }
        .block {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .emotions {
            font-size: 18px;
            font-weight: bold;
            color: #1d4ed8;
        }
        .message {
            font-size: 17px;
            color: #111827;
            line-height: 1.6;
        }
        .error {
            background-color: #fee2e2;
            color: #b91c1c;
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🕊️ SoulScribe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:#374151;'>Your Emotional Companion – Write your heart out.</p>", unsafe_allow_html=True)

user_input = st.text_area("How are you feeling today?", height=200, placeholder="Start journaling...")

if st.button("Reflect with Me"):
    if not user_input.strip():
        st.warning("Please write something before submitting.")
    else:
        with st.spinner("Analyzing your emotions..."):
            try:
                response = requests.post("http://127.0.0.1:5000/predict", json={"text": user_input})
                result = response.json()

                if "error" in result:
                    st.markdown(f"<div class='error'>{result['error']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='block'>", unsafe_allow_html=True)

                    st.markdown("### 🌈 Detected Emotions")
                    st.markdown(f"<div class='emotions'>{', '.join(result['emotions'])}</div>", unsafe_allow_html=True)

                    st.markdown("### 🧡 A Note for You")
                    st.markdown(f"<div class='message'>{result['message']}</div>", unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"<div class='error'>An error occurred:<br>{e}</div>", unsafe_allow_html=True)
