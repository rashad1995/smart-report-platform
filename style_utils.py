import streamlit as st
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def fix_ar(text):
    if not text: return ""
    # هذه الخطوة تعالج الحروف المقطعة والمقلوبة في الرسوم والعناوين
    reshaped_text = reshape(str(text))
    return get_display(reshaped_text)

def apply_custom_css():
    # حقن CSS عالمي لإجبار الصفحة كاملة على اتجاه اليمين
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        /* إجبار الاتجاه من اليمين لليسار لكل عناصر التطبيق */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stMarkdown {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Cairo', sans-serif;
        }

        /* تعديل اتجاه النصوص داخل الصناديق والمدخلات */
        div[data-baseweb="select"], .stTextInput, .stTextArea, .stSelectbox {
            direction: rtl !important;
            text-align: right !important;
        }

        /* تنسيق التقرير ليظهر كوثيقة رسمية عربية */
        .report-container {
            direction: rtl !important;
            text-align: right !important;
            background-color: #ffffff;
            padding: 35px;
            border-radius: 15px;
            border-right: 12px solid #1e3a8a; /* الخط الأزرق على اليمين */
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            line-height: 2;
        }

        /* قلب اتجاه الأعمدة (Columns) */
        [data-testid="column"] {
            direction: rtl !important;
            text-align: right !important;
        }
        </style>
        """, unsafe_allow_html=True)
