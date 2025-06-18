from flask import Flask, request, jsonify
import pdfplumber
import os
import uuid
import logging

app = Flask(__name__)

# Optional: Enable basic logging to Render logs
logging.basicConfig(level=logging.INFO)

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
            try:
                with pdfplumber.open(temp_path) as pdf:
                    for page_number, page in enumerate(pdf.pages, start=1):
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + '\n'
                            else:
                                logging.warning(f"No text found on page {page_number} of {file.filename}")
                        except Exception as page_err:
                            logging.error(f"Error extracting text from page {page_number} of {file.filename}: {page_err}")
            except Exception as file_err:
                logging.error(f"Error opening PDF file {file.filename}: {file_err}")
                os.remove(temp_path)
                continue  # Skip this file if it can't be opened

            os.remove(temp_path)

            results.append({
                'filename': file.filename,
                'text': text.strip()
            })

        return jsonify({'results': results}), 200

    except Exception as e:
        logging.error(f"Unhandled exception in extract_text: {e}")
        return jsonify({'error': str(e)}), 500
