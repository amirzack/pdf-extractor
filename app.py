from flask import Flask, request, render_template, send_file, session, redirect, url_for
import pdfplumber
import json
import os
import threading
import re
import unicodedata

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ZIPF_FILE_PATH = 'NGSL.json'

# Zipf data 
def load_zipf_data():
    with open(ZIPF_FILE_PATH, 'r') as file:
        data = json.load(file)
    zipf_data = {}
    for entry in data['NGSL_1.2_stats']:
        lemma = entry.get('Lemma')
        sfi = entry.get('SFI', 0)
        if isinstance(lemma, str):
            lemma = lemma.strip().lower()
            zipf_data[lemma] = sfi
    return zipf_data

# Extract Pdf

def process_pdf(file_path, zipf_data):
    with pdfplumber.open(file_path) as pdf:
        all_words = set()  
        for page in pdf.pages:
            text = page.extract_text()
            words = process_words(text, zipf_data)
            all_words.update(words)

        word_info = []
        for idx, word in enumerate(all_words, start=1):
            zipf_value = zipf_data.get(word, 0)
            # Filter word with zipf value 
            if zipf_value > 68:
                continue
            word_info.append({
                'id': idx,
                'word': word,
            })

        return word_info



# Word processing
def process_words(text, zipf_data):
    text = text.lower()

    words = re.findall(r'\b\w+\b', text)

    processed_words = []
    for word in words:
        #ِDelete char
        cleaned_word = ''.join(char for char in word if unicodedata.category(char) != 'Cn')

        # Delete word with 4 char
        if len(cleaned_word) >= 4:
            processed_words.append(cleaned_word)
    
    return processed_words

@app.route('/')
def upload_form():
    
    if session.get('processing_complete', False):
        return redirect(url_for('download_file', filename='word_analysis.json'))
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    zipf_data = load_zipf_data()

    # Preocessing in background
    def run_processing():
        processed_words = process_pdf(file_path, zipf_data)
        output_file_path = os.path.join(UPLOAD_FOLDER, 'word_analysis.json')
        with open(output_file_path, 'w') as f:
            json.dump(processed_words, f, ensure_ascii=False, indent=4)

        # Change session Status
        session['processing_complete'] = True

    threading.Thread(target=run_processing).start()

   #Save Process status intor session
    session['processing_complete'] = False

    return "File uploaded and is being processed. You will be notified when it's ready."

@app.route('/status')
def processing_status():
    if session.get('processing_complete', False):
        return redirect(url_for('download_file', filename='word_analysis.json'))
    else:
        return "Processing in progress. Please wait..."

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, 'word_analysis.json')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
