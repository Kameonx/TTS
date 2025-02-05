from flask import Flask, request, send_from_directory, render_template
from gtts import gTTS
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form.get('text')
    lang = request.form.get('lang', 'en')  # Default to 'en' if not found

    if not text:
        return "No text provided", 400

    # Map language codes to TLDs if necessary
    tld_map = {
        'en': 'com',
        'en-uk': 'co.uk',
        'en-au': 'com.au',
        'en-in': 'co.in',
        'es': 'com',
        'es-us': 'com',
        'fr': 'fr',
        'de': 'de',
    }

    tld = tld_map.get(lang, 'com')  # Default to 'com' if not found in the map

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"textToSpeech_{timestamp}.mp3"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    tts = gTTS(text=text, lang=lang, slow=False, tld=tld)
    tts.save(filepath)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
