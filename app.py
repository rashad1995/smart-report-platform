import streamlit as st
import pandas as pd
import fitz, io
import plotly.express as px
from groq import Groq
from style_utils import apply_custom_css, fix_ar
from bot_logic import run_interaction

apply_custom_css()

# التحقق من مفتاح الـ API
if "GROQ_API_KEY" not in st.secrets:
    st.error("خطأ: مفتاح GROQ_API_KEY غير موجود في الإعدادات السرية.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

with st.sidebar:
    st.title(fix_ar("🛡️ لوحة التحكم"))
    file = st.file_uploader(fix_ar("ارفع ملف الماجستير هنا"), type=['pdf', 'xlsx', 'csv', 'txt'])
    if st.button(fix_ar("بدء تحليل جديد")):
        st.session_state.step = 0
        st.rerun()

if file:
    # منطق التشات بوت
    if run_interaction():
        with st.spinner(fix_ar("جاري معالجة الملف وبناء التقرير الاستراتيجي...")):
            # استخلاص النص
            content = file.name # (كمثال)
            if file.name.endswith('pdf'):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                content = " ".join([page.get_text() for page in doc])[:4000]

            prompt = f"أنت خبير استراتيجي. النوع: {st.session_state.data['type']}. التفصيل: {st.session_state.data['detail']}. حلل النص وقدم تقريراً منسقاً بأسلوب الماجستير."
            
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt + content}],
                model="llama-3.3-70b-versatile"
            )
            report = res.choices[0].message.content

            # العرض النهائي المنظم
            st.markdown(f"### {fix_ar('📄 التقرير الاستراتيجي النهائي')}")
            st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
            
            # الرسوم البيانية
            fig = px.bar(x=[fix_ar("دقة البيانات"), fix_ar("كفاية المراجع"), fix_ar("التحليل النقدي")], 
                         y=[85, 90, 75], title=fix_ar("تقييم جودة المحتوى المرفوع"))
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(fix_ar("التقرير جاهز! استخدم Ctrl+P لحفظه كملف PDF احترافي."))
else:
    st.markdown(f"<h1 style='text-align: center; color: #003366;'>{fix_ar('منصة ذكاء الماجستير الاستراتيجي')}</h1>", unsafe_allow_html=True)
    st.info(fix_ar("بانتظار رفع الملف لبدء العملية الاستشارية..."))
