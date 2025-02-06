from flask import Flask, request, send_file, render_template, flash, redirect, url_for
from gtts import gTTS, gTTSError
from datetime import datetime
import os
import logging

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/Kameon2/TTS/downloads'  # Ensure this directory exists and is writable
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# List of supported gTTS language codes and their display names
supported_languages = {
    'en': 'English (US)',
    'en-gb': 'English (UK)',
    'en-au': 'English (Australia)',
    'en-in': 'English (India)',
    'es': 'Spanish (Spain)',
    'es-us': 'Spanish (US)',
    'fr': 'French (France)',
    'de': 'German (Germany)',
}

# Mapping of language codes to TLDs
language_to_tld = {
    'en': 'com',
    'en-gb': 'co.uk',
    'en-au': 'com.au',
    'en-in': 'co.in',
    'es': 'es',
    'es-us': 'us',
    'fr': 'fr',
    'de': 'de',
}

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html', supported_languages=supported_languages)

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form.get('text')
    lang = request.form.get('lang', 'en')  # Default to 'en' if not found

    logging.info(f"Received text: {text}")
    logging.info(f"Received language: {lang}")

    if not text:
        flash("No text provided", 'warning')
        return redirect(url_for('index'))

    if lang not in supported_languages:
        flash("Unsupported language selected", 'error')
        return redirect(url_for('index'))

    # Get the appropriate TLD for the selected language
    tld = language_to_tld.get(lang, 'com')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"textToSpeech_{timestamp}.mp3"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        # Ensure text is UTF-8 encoded
        text = text.encode('utf-8').decode('utf-8')
        tts = gTTS(text=text, lang=lang, tld=tld, slow=False, lang_check=True)
        tts.save(filepath)
        logging.info(f"File saved to: {filepath}")
        return send_file(filepath, as_attachment=True, download_name=filename)
    except gTTSError as e:
        logging.error(f"gTTS error: {str(e)} for language {lang} with TLD {tld}")
        flash(f"Error converting text to speech for language {lang} with TLD {tld}: {str(e)}", 'error')
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)} for language {lang} with TLD {tld}")
        flash(f"An unexpected error occurred for language {lang} with TLD {tld}: {str(e)}", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
