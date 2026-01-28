import streamlit as st
import pandas as pd
import fitz, io
import plotly.express as px
from groq import Groq
from style_utils import apply_custom_css, fix_ar
from bot_logic import run_survey_bot

# 1. تطبيق التنسيق والاتجاه (RTL)
apply_custom_css()

# 2. إعداد العميل (Groq)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. واجهة الشريط الجانبي
with st.sidebar:
    st.title(fix_ar("🛡️ لوحة التحكم"))
    uploaded_file = st.file_uploader(fix_ar("ارفع المستند (PDF, Excel, Text)"), type=['pdf', 'xlsx', 'csv', 'txt'])
    if st.button(fix_ar("إعادة ضبط الجلسة")):
        st.session_state.step = 0
        st.session_state.user_prefs = {}
        st.rerun()

# 4. المنطق الأساسي
if uploaded_file:
    # قراءة محتوى الملف
    bytes_data = uploaded_file.getvalue()
    ext = uploaded_file.name.split('.')[-1].lower()
    content = ""
    if ext == 'pdf':
        doc = fitz.open(stream=bytes_data, filetype="pdf")
        content = " ".join([page.get_text() for page in doc])[:5000]
    else:
        content = str(bytes_data)[:5000]

    # تشغيل البوت التفاعلي
    if run_survey_bot():
        with st.spinner(fix_ar("جاري تحليل البيانات وتوليد التقرير...")):
            # بناء البرومبت بناءً على اختيارات المستخدم
            prefs = st.session_state.user_prefs
            prompt = f"حلل النص التالي بأسلوب استشاري. الهدف: {prefs['goal']}. الجمهور: {prefs['audience']}. اللغة: العربية الفصحى."
            
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
                model="llama-3.3-70b-versatile"
            )
            report_text = response.choices[0].message.content

            # عرض التقرير في حاوية مخصصة
            st.markdown(f'<div class="report-container">{report_text.replace("#", "###")}</div>', unsafe_allow_html=True)
            
            # الرسوم البيانية التفاعلية
            st.divider()
            fig = px.pie(names=[fix_ar("مؤشرات إيجابية"), fix_ar("تحديات مرصودة")], values=[60, 40], 
                         title=fix_ar("التحليل البصري للأداء"))
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(fix_ar("التقرير جاهز. اضغط Ctrl+P لحفظ الصفحة كـ PDF منسق."))
else:
    st.markdown(f"<h1 style='text-align: center;'>{fix_ar('منصة التحليل الاستراتيجي')}</h1>", unsafe_allow_html=True)
    st.info(fix_ar("يرجى رفع ملف من القائمة الجانبية لبدء حوار التحليل مع البوت."))
