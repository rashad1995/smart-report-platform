import os
import fitz  # PyMuPDF
import pandas as pd
from flask import Flask, render_template, request, jsonify
from groq import Groq
from arabic_reshaper import reshape
from bidi.algorithm import get_display

app = Flask(__name__)

# مفتاحك الذي وضعته في الكود
client = Groq(api_key="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")

def fix_ar(text):
    try:
        return get_display(reshape(str(text)))
    except:
        return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'لم يتم رفع ملف'})
    
    file = request.files['file']
    structure = request.form.get('structure', 'شامل')
    
    # معالجة الملف (نفس منطقك الأصلي)
    content_summary = ""
    ext = file.filename.split('.')[-1].lower()
    
    if ext == 'pdf':
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = " ".join([page.get_text() for page in doc])
        content_summary = text[:3000]
    elif ext in ['csv', 'xlsx']:
        df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)
        content_summary = df.describe().to_string()

    # طلب التحليل من Groq
    sys_prompt = f"أنت محلل خبير. التقرير مطلوب بهيكل {structure}. اللغة: العربية."
    completion = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_prompt},
                  {"role": "user", "content": f"حلل: {content_summary}"}],
        model="llama-3.3-70b-versatile"
    )
    report = completion.choices[0].message.content
    return jsonify({'report': report})

if __name__ == '__main__':
    app.run()
