
from flask import Flask, request, jsonify
import pdfplumber
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    text_data = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    text_data.append({'page': i+1, 'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)

    return jsonify({'pages': text_data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
