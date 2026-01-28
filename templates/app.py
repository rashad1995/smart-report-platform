from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# استدعاء المفتاح من البيئة (أو وضعه مباشرة مؤقتاً)
client = Groq(api_key="ضع_مفتاحك_هنا")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    goal = data.get('goal')
    audience = data.get('audience')
    
    # بناء البرومبت الاحترافي
    prompt = f"أنت مستشار استراتيجي. الهدف: {goal}. الجمهور: {audience}. حلل المعطيات وقدم تقريراً باللغة العربية الفصحى بتنسيق HTML (استخدم <h3> للعنوان و <ul> للنقاط)."
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        report = completion.choices[0].message.content
        return jsonify({'success': True, 'report': report})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
