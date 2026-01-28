import streamlit as st
from style_utils import fix_ar

def run_interaction():
    if 'step' not in st.session_state: st.session_state.step = 0
    if 'data' not in st.session_state: st.session_state.data = {}

    st.markdown(f"""<div class='chat-container'>
        <span style='font-size: 35px;'>🤖</span>
        <div><b>{fix_ar("المساعد الذكي:")}</b><br>{fix_ar("أهلاً بك في مرحلة تخصيص التقرير. يرجى تزويدي بالمعلومات التالية:")}</div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.step == 0:
        q1 = st.selectbox(fix_ar("1. ما هو نوع التحليل المطلوب؟"), 
                         [fix_ar("تحليل SWOT (قوة، ضعف، فرص، مخاطر)"), 
                          fix_ar("تحليل مالي وميزانية"), 
                          fix_ar("ملخص أكاديمي لنقد الرسالة")])
        if st.button(fix_ar("تثبيت الاختيار والذهاب للسؤال التالي ⬅️")):
            st.session_state.data['type'] = q1
            st.session_state.step = 1
            st.rerun()

    elif st.session_state.step == 1:
        q2 = st.radio(fix_ar("2. ما هو مستوى التفصيل؟"), 
                     [fix_ar("موجز للمناقشة"), fix_ar("تقرير استشاري موسع")])
        if st.button(fix_ar("إرسال البيانات وتوليد التقرير النهائي ✨")):
            st.session_state.data['detail'] = q2
            st.session_state.step = 2
            st.rerun()
    
    return st.session_state.step == 2
