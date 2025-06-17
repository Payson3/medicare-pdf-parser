# Medicare PDF Parser

A Flask-based microservice that extracts structured text from Medicare Advantage plan PDF files using PyMuPDF (`fitz`). Designed for integration with no-code platforms like n8n and web tools such as Loveable.

## Features

- Accepts PDF uploads via HTTP POST
- Extracts and returns raw text content for AI/LLM workflows
- Lightweight and fast using `PyMuPDF`
- Easily deployable on platforms like Render or Fly.io

## Tech Stack

- Python 3.x
- Flask
- PyMuPDF (`fitz`)

## Local Setup (for testing)

```bash
git clone https://github.com/yourusername/medicare-pdf-parser.git
cd medicare-pdf-parser
python -m venv venv
venv\Scripts\activate    # On Windows
pip install -r requirements.txt
python app.py              # or pdf_extractor_service.py
```

Flask should now be running on:
```
http://127.0.0.1:8080/extract
```

## API Endpoint

### POST `/extract`

**Content-Type**: `multipart/form-data`  
**Body**:  
- `file`: PDF file upload

**Response**:
```json
{
  "text": "Extracted text from PDF..."
}
```

## Example `curl` Command

```bash
curl -X POST http://127.0.0.1:8080/extract -F "file=@"./your-pdf-file.pdf""
```

## Deployment (Render)

1. Push this repo to GitHub.
2. Go to [https://dashboard.render.com](https://dashboard.render.com)
3. Click "New Web Service"
4. Connect your GitHub repo.
5. Set the build and start commands:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Set the port to **8080**
7. Deploy.

## License

MIT License
