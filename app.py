import streamlit as st
import pandas as pd
import fitz
import plotly.express as px
from style_utils import apply_custom_css, fix_ar
from bot_logic import run_interactive_bot
from ai_engine import generate_report

# 1. تطبيق التنسيق
apply_custom_css()

# 2. الواجهة الجانبية
with st.sidebar:
    st.title(fix_ar("لوحة التحكم"))
    file = st.file_uploader(fix_ar("ارفع ملفك هنا"), type=['pdf', 'xlsx', 'csv', 'txt'])
    if st.button(fix_ar("إعادة التحليل")):
        st.session_state.step = 0
        st.rerun()

# 3. المنطق الرئيسي
if file:
    # قراءة سريعة للملف
    content = file.name # تبسيط للمثال
    if run_interactive_bot():
        with st.spinner(fix_ar("جاري بناء التقرير...")):
            report = generate_report(content, st.session_state.user_prefs)
            
            st.markdown(f'<div class="report-container">{report.replace("#", "###")}</div>', unsafe_allow_html=True)
            
            # الرسوم البيانية
            fig = px.pie(names=[fix_ar("إيجابيات"), fix_ar("تحديات")], values=[65, 35], hole=0.4)
            st.plotly_chart(fig)
            
            st.success(fix_ar("التقرير جاهز! اضغط Ctrl+P لحفظه كـ PDF مع المخططات."))
else:
    st.header(fix_ar("مرحباً بك في منصتك الاستشارية"))
