import streamlit as st
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def fix_ar(text):
    if not text: return ""
    # تصحيح تشكيل الحروف العربية ثم عكس الاتجاه للعرض الصحيح
    return get_display(reshape(str(text)))

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
        
        /* إجبار التطبيق بالكامل على اتجاه اليمين لليسار */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stMarkdown {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Cairo', sans-serif !important;
        }
        
        /* تنسيق "كرت" التقرير الاستراتيجي */
        .report-box {
            background-color: #fcfcfc;
            padding: 40px;
            border-radius: 20px;
            border-right: 15px solid #003366;
            box-shadow: 0 15px 40px rgba(0,0,0,0.08);
            margin: 25px 0;
            line-height: 2.2;
            color: #1a1a1a;
            white-space: pre-wrap; /* للحفاظ على تنسيق الأسطر */
        }

        /* تحسين مظهر التشات بوت */
        .chat-container {
            background: #e9ecef;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
            gap: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
