import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import io, fitz, base64
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# --- 1. هندسة الواجهة العربية (الضبط الجذري) ---
st.set_page_config(page_title="AI Strategic Advisor", layout="wide")

def fix_ar(text):
    if not text: return ""
    return get_display(reshape(str(text)))

# حقن CSS مكثف لإجبار المتصفح على اتجاه اليمين لليسار (RTL) وتنسيق البوت
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif;
    }
    .stMarkdown, .stButton, .stSelectbox, .stRadio, div[data-baseweb="select"] {
        direction: rtl !important;
        text-align: right !important;
    }
    /* تنسيق كرت التقرير */
    .report-container {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        border-right: 10px solid #1e3a8a;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    /* أيقونة البوت */
    .bot-header {
        display: flex;
        align-items: center;
        background: #f0f2f6;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك Groq ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. إدارة حالة الجلسة (للبوت التفاعلي) ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = {}

# --- 4. الشريط الجانبي ---
with st.sidebar:
    st.markdown(f"## {fix_ar('القائمة الرئيسية')}")
    uploaded_file = st.file_uploader(fix_ar("ارفع الملف المراد تحليله"), type=['pdf', 'xlsx', 'csv', 'txt'])
    if st.button(fix_ar("إعادة تعيين التحليل")):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()

# --- 5. منطق العمل الرئيسي ---
if uploaded_file:
    # قراءة الملف
    content = ""
    ext = uploaded_file.name.split('.')[-1].lower()
    if ext == 'pdf':
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        content = " ".join([page.get_text() for page in doc])[:5000]
    elif ext in ['xlsx', 'csv']:
        df = pd.read_csv(uploaded_file) if ext == 'csv' else pd.read_excel(uploaded_file)
        content = df.to_string()[:5000]

    # --- أيقونة وتشات بوت الأسئلة ---
    st.markdown(f"""
        <div class="bot-header">
            <span style='font-size: 40px; margin-left: 15px;'>🤖</span>
            <div>
                <h3 style='margin:0;'>{fix_ar("المساعد الذكي (التشخيص التمهيدي)")}</h3>
                <p style='margin:0; color: #666;'>{fix_ar("ساعدني لأفهم متطلباتك بدقة قبل توليد التقرير")}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # نظام الأسئلة متسلسل
    if st.session_state.step == 0:
        q1 = st.radio(fix_ar("1. ما هو الهدف الأساسي من هذا التحليل؟"), 
                     [fix_ar("تحديد نقاط الضعف والمخاطر"), fix_ar("استكشاف فرص استثمارية"), fix_ar("مراجعة الأداء الأكاديمي")])
        if st.button(fix_ar("التالي")):
            st.session_state.answers['goal'] = q1
            st.session_state.step = 1
            st.rerun()

    elif st.session_state.step == 1:
        q2 = st.radio(fix_ar("2. ما هو أسلوب الصياغة المفضل؟"), 
                     [fix_ar("تنفيذي مختصر"), fix_ar("تحليلي مفصل"), fix_ar("نقد أكاديمي")])
        if st.button(fix_ar("توليد التقرير النهائي 🚀")):
            st.session_state.answers['style'] = q2
            st.session_state.step = 2
            st.rerun()

    # --- توليد التقرير النهائي ---
    if st.session_state.step == 2:
        with st.spinner(fix_ar('جاري المعالجة...')):
            ans = st.session_state.answers
            prompt = f"أنت خبير استراتيجي. الهدف: {ans['goal']}. الأسلوب: {ans['style']}. حلل النص التالي وقدم تقريراً منسقاً بالعناوين:"
            
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
                model="llama-3.3-70b-versatile"
            )
            full_report = res.choices[0].message.content

            # عرض التقرير
            st.markdown(f'<div class="report-container">{full_report.replace("#", "###")}</div>', unsafe_allow_html=True)

            # الرسوم البيانية (Plotly تفاعلي)
            st.divider()
            fig = px.bar(x=[fix_ar("مخاطر"), fix_ar("فرص"), fix_ar("قوة")], y=[30, 70, 50], 
                         title=fix_ar("مخطط الأهمية النسبية"), color_discrete_sequence=['#1e3a8a'])
            st.plotly_chart(fig, use_container_width=True)

            # --- تصدير PDF (عبر المتصفح) ---
            st.info(fix_ar("لحفظ التقرير والمخططات كـ PDF احترافي: اضغط Ctrl + P (أو Cmd + P) واختر Save as PDF. الواجهة مهيأة للطباعة."))

else:
    st.markdown(f"<h1 style='text-align: center;'>{fix_ar('منصة التحليل الاستراتيجي الاحترافية')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{fix_ar('يرجى رفع الملف لبدء الحوار مع البوت الذكي')}</p>", unsafe_allow_html=True)
