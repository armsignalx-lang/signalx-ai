import os, json, io
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "signalx_2026_key")

# Gemini API Կարգավորում
API_KEY = "AIzaSyD1c-Qx75ItMfcZmnWq91gdSMaCyhhqBz0"
genai.configure(api_key=API_KEY)

TRANSLATIONS = {
    'ai_analysis': 'AI Վերլուծություն',
    'decision': 'ՈՐՈՇՈՒՄ',
    'confidence': 'ՀԱՄՈԶՎԱԾՈՒԹՅՈՒՆ',
    'reason': 'ՊԱՏՃԱՌ'
}

@app.route('/')
def home():
    return render_template('signals_page.html', lang=TRANSLATIONS)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files.get('image')
        if not file:
            return jsonify({"decision": "WAIT", "conf": "0", "reason": "Նկարը չկա"})

        # Նկարի մշակում
        img = Image.open(io.BytesIO(file.read()))
        
        # Մոդելի ընտրություն (ստույգ անվանումը)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = "Analyze this binary options chart. Check RSI, Stochastic and Vortex. Return ONLY JSON: {'decision': 'CALL/PUT', 'conf': '85', 'reason': 'Armenian description of indicators'}"
        
        # Հարցում Gemini-ին
        response = model.generate_content([prompt, img])
        res_text = response.text.strip()

        # JSON զտում տեքստից
        if "{" in res_text:
            res_text = res_text[res_text.find("{"):res_text.rfind("}")+1]
        
        return jsonify(json.loads(res_text))
    except Exception as e:
        # Սխալի մանրամասն արտածում հասկանալու համար
        return jsonify({"decision": "ERROR", "conf": "0", "reason": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
