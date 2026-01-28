import streamlit as st
from style_utils import fix_ar

def run_interactive_bot():
    if 'step' not in st.session_state: st.session_state.step = 0
    if 'user_prefs' not in st.session_state: st.session_state.user_prefs = {}

    st.markdown(f"""
        <div class="bot-header">
            <span style='font-size: 40px; margin-left: 15px;'>🤖</span>
            <div>
                <h3 style='margin:0;'>{fix_ar("المساعد الذكي")}</h3>
                <p style='margin:0; color: #555;'>{fix_ar("أجب على الأسئلة لضبط معايير التقرير")}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.step == 0:
        choice = st.radio(fix_ar("1. ما هي طبيعة الملف المرفوع؟"), 
                         [fix_ar("بيانات مالية وأرقام"), fix_ar("نصوص وأبحاث نظرية"), fix_ar("خطة عمل استراتيجية")])
        if st.button(fix_ar("التالي ⬅️")):
            st.session_state.user_prefs['type'] = choice
            st.session_state.step = 1
            st.rerun()

    elif st.session_state.step == 1:
        choice = st.radio(fix_ar("2. ما هو مستوى النقد المطلوب في التقرير؟"), 
                         [fix_ar("إيجابي ومحفز"), fix_ar("نقد موضوعي صارم"), fix_ar("تحليل شامل (SWOT)")])
        if st.button(fix_ar("توليد التقرير النهائي 🚀")):
            st.session_state.user_prefs['mood'] = choice
            st.session_state.step = 2
            st.rerun()
    
    return st.session_state.step == 2
