from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import os
import uuid
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/extract', methods=['POST'])
def extract_text():
    try:
        if not request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        results = []

        # Convert ImmutableMultiDict to standard dict with list values
        files_dict = request.files.to_dict(flat=False)

        # Iterate through all files under all keys (e.g., 'data', 'data1', 'data2')
        for key in files_dict:
            for file in files_dict[key]:
                filename = f"{uuid.uuid4()}_{file.filename}"
                temp_path = os.path.join('/tmp', filename)
                file.save(temp_path)

                text = ''
                try:
                    doc = fitz.open(temp_path)
                    for page_number, page in enumerate(doc, start=1):
                        try:
                            page_text = page.get_text("text")
                            if page_text:
                                text += page_text + '\n'
                            else:
                                logging.warning(f"No text on page {page_number} of {file.filename}")
                        except Exception as page_err:
                            logging.error(f"Error on page {page_number} of {file.filename}: {page_err}")
                    doc.close()
                except Exception as file_err:
                    logging.error(f"Error opening PDF {file.filename}: {file_err}")
                    os.remove(temp_path)
                    continue  # Skip this file if unreadable

                os.remove(temp_path)

                results.append({
                    'filename': file.filename,
                    'text': text.strip()
                })

        return jsonify({'results': results}), 200

    except Exception as e:
        logging.error(f"Unhandled exception in extract_text: {e}")
        return jsonify({'error': str(e)}), 500
