import streamlit as st
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def fix_ar(text):
    if not text: return ""
    # معالجة النصوص العربية لضمان عدم ظهور الحروف مقطعة
    return get_display(reshape(str(text)))

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* ضبط اتجاه التطبيق بالكامل من اليمين لليسار */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stMarkdown {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Cairo', sans-serif;
        }
        
        /* تنسيق كرت التقرير الاحترافي */
        .report-container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            border-right: 10px solid #1e3a8a;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            margin: 20px 0;
            line-height: 2;
            color: #2c3e50;
        }
        
        /* تنسيق أيقونة البوت */
        .bot-bubble {
            background: #f0f2f6;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #d1d9e6;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        /* تحسين مظهر الأزرار */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            background-color: #1e3a8a;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
