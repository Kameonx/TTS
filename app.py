from flask import Flask, request, send_file, render_template, flash, redirect, url_for, make_response
from gtts import gTTS, gTTSError
from datetime import datetime
from io import BytesIO
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure secret key

# Supported languages and their display names
supported_languages = {
    'en': 'US',
    'en-gb': 'UK',
    'en-au': 'Australia',
    'en-in': 'India',
    'es': 'Spain',
    'es-us': 'Spanish (US)',
    'fr': 'France',
    'de': 'Germany',
}

# Language code to Google TLD mapping
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
    try:
        # Get form data
        text = request.form['text'].strip()
        lang = request.form.get('lang', 'en')

        # Validate input
        if not text:
            flash("Please enter some text to convert", 'warning')
            return redirect(url_for('index'))
            
        if lang not in supported_languages:
            flash("Unsupported language selected", 'error')
            return redirect(url_for('index'))

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"textToSpeech_{timestamp}.mp3"

        # Create in-memory audio file
        audio_buffer = BytesIO()
        tts = gTTS(
            text=text,
            lang=lang,
            tld=language_to_tld.get(lang, 'com'),
            slow=False
        )
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        # Create response with proper headers
        response = make_response(audio_buffer.read())
        response.headers['Content-Type'] = 'audio/mpeg'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response

    except KeyError:
        flash("Invalid form submission", 'error')
        return redirect(url_for('index'))
    except gTTSError as e:
        logging.error(f"gTTS Error: {str(e)}")
        flash(f"Conversion error: {str(e)}", 'error')
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        flash(f"An unexpected error occurred: {str(e)}", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
