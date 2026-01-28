from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key="ضع_مفتاحك_هنا")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.form.get('context') # إجابات التشات بوت
    # هنا نرسل لـ Groq
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": f"حلل بأسلوب أكاديمي: {user_input}"}],
        model="llama-3.3-70b-versatile"
    )
    return jsonify({'report': completion.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)
