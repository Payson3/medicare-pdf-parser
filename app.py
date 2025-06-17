from flask import Flask, request, jsonify
import pdfplumber
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_text():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        temp_path = os.path.join('/tmp', filename)
        file.save(temp_path)

        text = ''
        with pdfplumber.open(temp_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ''

        os.remove(temp_path)
        return jsonify({'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

