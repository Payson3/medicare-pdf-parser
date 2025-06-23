from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import io

app = Flask(__name__)
CORS(app)

# Set max request size to 32 MB
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB

@app.route("/extract", methods=["POST"])
def extract_text():
    try:
        pdf_files = request.files.to_dict()
        results = []

        for field_name, file_storage in pdf_files.items():
            file_bytes = file_storage.read()
            pdf = fitz.open(stream=file_bytes, filetype="pdf")
            text = "\n".join([page.get_text() for page in pdf])
            results.append({
                "filename": file_storage.filename,
                "text": text
            })

        return jsonify(results)
    
    except Exception as e:
        app.logger.error(f"Unhandled exception in extract_text: {str(e)}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

# Handle file too large error
@app.errorhandler(413)
def too_large(e):
    return jsonify(error="File too large", message=str(e)), 413

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
