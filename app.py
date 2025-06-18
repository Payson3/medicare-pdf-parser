from flask import Flask, request, jsonify
import pdfplumber
import os

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_text():
    try:
        if not request.files:
            return jsonify({'error': 'No files in the request'}), 400

        extracted_data = []

        for key in request.files:
            file = request.files[key]
            if not file or file.filename == '':
                continue

            temp_path = os.path.join('/tmp', file.filename)
            file.save(temp_path)

            text = ''
            with pdfplumber.open(temp_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ''

            os.remove(temp_path)

            extracted_data.append({
                'filename': file.filename,
                'text': text
            })

        if not extracted_data:
            return jsonify({'error': 'No valid PDFs processed'}), 400

        return jsonify({'documents': extracted_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
