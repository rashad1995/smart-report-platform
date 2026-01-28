import streamlit as st
from style_utils import fix_ar

def run_survey_bot():
    if 'step' not in st.session_state: st.session_state.step = 0
    if 'user_prefs' not in st.session_state: st.session_state.user_prefs = {}

    st.markdown(f"""
        <div class="bot-bubble">
            <span style='font-size: 30px;'>🤖</span>
            <div>
                <strong>{fix_ar("المساعد الذكي:")}</strong><br>
                {fix_ar("أهلاً بك! يرجى الإجابة على الأسئلة لتخصيص التقرير.")}
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.step == 0:
        q1 = st.radio(fix_ar("1. ما هو الغرض من هذا التحليل؟"), 
                     [fix_ar("تقييم المخاطر"), fix_ar("فرص التطوير"), fix_ar("ملخص أكاديمي")])
        if st.button(fix_ar("السؤال التالي ⬅️")):
            st.session_state.user_prefs['goal'] = q1
            st.session_state.step = 1
            st.rerun()

    elif st.session_state.step == 1:
        q2 = st.radio(fix_ar("2. من هو الجمهور المستهدف؟"), 
                     [fix_ar("لجنة المناقشة"), fix_ar("إدارة عليا"), fix_ar("مختصون تقنيون")])
        if st.button(fix_ar("توليد التقرير النهائي 🚀")):
            st.session_state.user_prefs['audience'] = q2
            st.session_state.step = 2
            st.rerun()
    
    return st.session_state.step == 2
