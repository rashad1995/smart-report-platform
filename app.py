import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import io, fitz, re
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# --- إعدادات الصفحة ---
st.set_page_config(page_title="AI Strategy Hub", layout="wide")

# --- محرك التنسيق واللغة ---
lang = st.sidebar.selectbox("🌐 لغة التقرير / Report Language", ["العربية", "English"])
is_ar = lang == "العربية"
align = "right" if is_ar else "left"
direction = "rtl" if is_ar else "ltr"

def fix_text(text):
    if is_ar:
        return get_display(reshape(str(text)))
    return text

# --- التنسيق البصري (CSS) ---
st.markdown(f"""
    <style>
    .report-card {{
        background: white; padding: 25px; border-radius: 15px;
        border-right: 5px solid #1e3a8a; border-left: {"none" if is_ar else "5px solid #1e3a8a"};
        direction: {direction}; text-align: {align};
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); line-height: 1.8;
    }}
    .section-header {{ color: #1e3a8a; font-weight: bold; border-bottom: 2px solid #e2e8f0; margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- استدعاء العميل ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- الواجهة الجانبية ---
with st.sidebar:
    st.title("🛡️ Pro Analyzer")
    uploaded_file = st.file_uploader("📂 ارفع ملفك (PDF, CSV, XLSX, TXT)", type=['pdf', 'csv', 'xlsx', 'txt'])
    
if uploaded_file:
    # 1. قراءة الملف (دعم كافة الأنواع)
    bytes_data = uploaded_file.getvalue()
    ext = uploaded_file.name.split('.')[-1].lower()
    
    if ext == 'pdf':
        doc = fitz.open(stream=bytes_data, filetype="pdf")
        content = " ".join([page.get_text() for page in doc])[:5000]
    elif ext in ['csv', 'xlsx']:
        df = pd.read_csv(io.BytesIO(bytes_data)) if ext == 'csv' else pd.read_excel(io.BytesIO(bytes_data))
        content = df.head(20).to_string()
    else:
        content = bytes_data.decode("utf-8")[:5000]

    # 2. الاستبيان الذكي (التشات بوت التمهيدي)
    st.info("🎯 يرجى تحديد معايير التحليل المطلوبة لضبط المحرك:" if is_ar else "🎯 Set analysis criteria:")
    
    col1, col2 = st.columns(2)
    with col1:
        focus = st.radio(fix_text("تركيز التحليل:"), [fix_text("مالي"), fix_text("تشغيلي"), fix_text("استراتيجي")])
    with col2:
        risk_level = st.radio(fix_text("مستوى تقييم المخاطر:"), [fix_text("منخفض"), fix_text("متوسط"), fix_text("عميق")])

    if st.button("🚀 توليد التقرير النهائي" if is_ar else "🚀 Generate Final Report"):
        with st.spinner('جاري صياغة التقرير حسب تفضيلاتك...'):
            # بناء البرومبت بناءً على إجابات المستخدم
            sys_msg = f"Role: Expert Consultant. Language: {lang}. Context: Focus on {focus} with {risk_level} risk analysis."
            user_msg = f"Analyze this content and provide a structured report with headers: {content}"
            
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": user_msg}],
                model="llama-3.3-70b-versatile"
            )
            report = res.choices[0].message.content

            # 3. عرض التقرير بتنسيق ملون
            st.markdown(f"""
                <div class="report-card">
                    <div class="section-header"><h2>{fix_text("النتائج النهائية للتحليل")}</h2></div>
                    {report.replace("#", "").replace("**", "<b>").replace("\n", "<br>")}
                </div>
            """, unsafe_allow_html=True)

            # 4. الرسوم البيانية التفاعلية
            fig = px.treemap(path=[[fix_text("التحليل")], [fix_text(focus)]], values=[100], title=fix_text("هيكل التركيز التحليلي"))
            st.plotly_chart(fig, use_container_width=True)

            # 5. التصدير (PDF)
            # ملاحظة: لتصدير PDF حقيقي مع مخططات نحتاج لمكتبة مثل fpdf أو reportlab
            st.download_button("📥 تصدير التقرير (Text/PDF Ready)", report, file_name="Strategic_Report.txt")

else:
    st.header(fix_text("مرحباً بك في منصة التحليل المتقدمة"))
    st.write(fix_text("ابدأ برفع الملف لتفعيل نظام الاستبيان الذكي."))
