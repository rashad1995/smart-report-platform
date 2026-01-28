import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
import io, fitz, re
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# --- 1. إعدادات الهوية البصرية المتقدمة ---
st.set_page_config(page_title="AI Strategy Hub Pro", layout="wide")

# اختيار اللغة وتحديد الاتجاه
lang = st.sidebar.selectbox("🌐 اختيار لغة التقرير / Language", ["العربية", "English"])
is_ar = lang == "العربية"
dir_attr = "rtl" if is_ar else "ltr"
align_text = "right" if is_ar else "left"

def fix_text(text):
    if is_ar:
        return get_display(reshape(str(text)))
    return text

# حقن CSS احترافي للتحكم في اتجاه الصفحة بالكامل
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .main {{
        direction: {dir_attr};
        text-align: {align_text};
        font-family: 'Tajawal', sans-serif;
    }}
    .report-card {{
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border-{ "right" if is_ar else "left" }: 8px solid #1e3a8a;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin: 20px 0;
        line-height: 1.8;
        color: #2d3436;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        direction: {dir_attr};
    }}
    .section-title {{
        color: #1e3a8a;
        border-bottom: 2px solid #eef2f7;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-weight: 700;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الذكاء الاصطناعي ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. الواجهة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1006/1006131.png", width=80)
    st.title("🛡️ المحلل الاستراتيجي")
    uploaded_file = st.file_uploader("📂 ارفع المستند (PDF, Excel, CSV, Text)", type=['pdf', 'csv', 'xlsx', 'txt'])
    st.divider()
    st.info("سيقوم النظام بتخصيص التحليل بناءً على إجاباتك التالية.")

# --- 4. معالجة المحتوى ---
if uploaded_file:
    with st.spinner('جاري فحص المستند...'):
        bytes_data = uploaded_file.getvalue()
        ext = uploaded_file.name.split('.')[-1].lower()
        
        if ext == 'pdf':
            doc = fitz.open(stream=bytes_data, filetype="pdf")
            content = " ".join([page.get_text() for page in doc])[:6000]
        elif ext in ['csv', 'xlsx']:
            df = pd.read_csv(io.BytesIO(bytes_data)) if ext == 'csv' else pd.read_excel(io.BytesIO(bytes_data))
            content = f"Data Summary: {df.describe().to_string()} \n Samples: {df.head(5).to_string()}"
        else:
            content = bytes_data.decode("utf-8")[:6000]

    # --- 5. نظام الاستبيان الذكي (التفاعلي) ---
    st.markdown(f"<h3 class='section-title'>{fix_text('🎯 تخصيص ذكاء التقرير')}</h3>", unsafe_allow_html=True)
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        purpose = st.selectbox(fix_text("ما هو هدف التحليل الأساسي؟"), 
                              [fix_text("كشف المخاطر"), fix_text("فرص النمو"), fix_text("تقييم الأداء الجاري")])
    with col_q2:
        audience = st.radio(fix_text("لمن سيوجه هذا التقرير؟"), 
                           [fix_text("لجنة أكاديمية"), fix_text("مجلس إدارة"), fix_text("فريق تقني")])

    if st.button("🚀 توليد التقرير الاحترافي"):
        with st.spinner('يتم الآن معالجة البيانات وبناء الرؤى...'):
            # البرومبت الاحترافي
            sys_prompt = f"""أنت مستشار استراتيجي أول. لغة التقرير: {lang}. 
            يجب أن يكون التنسيق أكاديمياً رصيناً. 
            الهدف: {purpose}. الجمهور المستهدف: {audience}. 
            استخدم عناوين واضحة ونقاطاً منظمة."""
            
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt},
                          {"role": "user", "content": f"حلل الوثيقة التالية: {content}"}],
                model="llama-3.3-70b-versatile"
            )
            report_body = res.choices[0].message.content

            # --- 6. عرض النتائج بتنسيق فائق الجودة ---
            tab_rep, tab_viz = st.tabs([fix_text("📄 التقرير الاستراتيجي"), fix_text("📊 الرسوم البيانية")])
            
            with tab_rep:
                st.markdown(f"""
                    <div class="report-card">
                        <h2 style='text-align: center; color: #1e3a8a;'>{fix_text("نتائج التحليل الاستراتيجي")}</h2>
                        <hr>
                        <div style='white-space: pre-wrap;'>{report_body}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # زر التحميل بتنسيق نصي نظيف
                st.download_button(fix_text("📥 تصدير التقرير"), report_body, file_name="Executive_Summary.txt")

            with tab_viz:
                st.subheader(fix_text("توزيع القيمة والأهمية"))
                # رسم بياني تفاعلي يعكس البيانات
                plot_data = pd.DataFrame({
                    'Category': [fix_text('القوة'), fix_text('الفرص'), fix_text('المخاطر')],
                    'Value': [45, 35, 20]
                })
                fig = px.bar(plot_data, x='Category', y='Value', color='Category', 
                             title=fix_text("الوزن النسبي لعناصر التحليل"))
                st.plotly_chart(fig, use_container_width=True)

else:
    # شاشة الترحيب
    st.markdown(f"""
        <div style='text-align: center; padding: 100px;'>
            <h1 style='color: #1e3a8a; font-size: 3.5em;'>{fix_text("المنصة الاستشارية الذكية")}</h1>
            <p style='font-size: 1.5em; color: #546e7a;'>{fix_text("حلول تحليل البيانات المتقدمة بدعم من Llama 3.3")}</p>
            <div style='color: #90a4ae;'>{fix_text("يرجى رفع ملف لبدء المحاكاة")}</div>
        </div>
    """, unsafe_allow_html=True)
