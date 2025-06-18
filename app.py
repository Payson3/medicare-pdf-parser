from flask import Flask, request, jsonify
import pdfplumber
import os
import uuid

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_text():
    try:
        if not request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        results = []
        for key in request.files:
            file = request.files[key]
            filename = f"{uuid.uuid4()}_{file.filename}"
            temp_path = os.path.join('/tmp', filename)
            file.save(temp_path)

            text = ''
            with pdfplumber.open(temp_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ''

            os.remove(temp_path)
            results.append({
                'filename': file.filename,
                'text': text.strip()
            })

        return jsonify({'results': results}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
