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
    text = request.form['text']
    if not text:
        return "No text provided", 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"textToSpeech_{timestamp}.mp3"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    tts = gTTS(text=text, lang="en", slow=False, tld="com.au")
    tts.save(filepath)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)