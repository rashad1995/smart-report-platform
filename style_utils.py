import streamlit as st
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def fix_ar(text):
    if not text: return ""
    return get_display(reshape(str(text)))

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Cairo', sans-serif;
        }
        .report-container {
            background-color: #ffffff; padding: 30px; border-radius: 20px;
            border-right: 10px solid #1e3a8a; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            line-height: 1.8; color: #333;
        }
        .bot-header {
            display: flex; align-items: center; background: #eef2f7;
            padding: 20px; border-radius: 15px; margin-bottom: 25px;
            border: 1px solid #d1d9e6;
        }
        @media print {
            .stButton, .stSidebar, .stDownloadButton { display: none !important; }
            .report-container { border: none; box-shadow: none; }
        }
        </style>
        """, unsafe_allow_html=True)
