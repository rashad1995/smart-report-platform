import streamlit as st
from groq import Groq

def generate_report(content, prefs):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    prompt = f"""
    Role: Expert Strategic Consultant.
    Language: Arabic (Modern Standard).
    Context: The user uploaded a {prefs['type']} and wants a {prefs['mood']} analysis.
    Task: Write a structured professional report with headings and clear insights.
    """
    
    completion = client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
        model="llama-3.3-70b-versatile"
    )
    return completion.choices[0].message.content
