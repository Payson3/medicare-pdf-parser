from flask import Flask, request, jsonify
import pdfplumber
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_text():
    try:
        # Check if any files were sent
        if not request.files:
            return jsonify({'error': 'No files found in request'}), 400

        extracted_results = []

        for key in request.files:
            file = request.files[key]
            if file.filename == '':
                continue  # skip if filename is empty

            filename = secure_filename(file.filename)
            temp_path = os.path.join('/tmp', filename)
            file.save(temp_path)

            text = ''
            with pdfplumber.open(temp_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ''

            os.remove(temp_path)

            extracted_results.append({
                'filename': filename,
                'text': text
            })

        if not extracted_results:
            return jsonify({'error': 'No valid files were processed'}), 400

        return jsonify({'documents': extracted_results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


