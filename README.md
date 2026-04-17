# Trade Opportunities API

A FastAPI service that analyzes market data and provides trade opportunity insights for specific sectors in India.

## Features
- Analyzes market sectors using recent news and data.
- Structured Markdown report generated using Google Gemini API.
- Integrated rate limiting (`5 requests / minute` per IP).
- API Key Authentication (`X-API-Key` header).
- In-memory processing without a database.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Pip

### 2. Installation
Clone the repository, navigate into the directory, and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Fill in your Google Gemini API Key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
API_KEY=your_secret_api_key_here
```

### 4. Running the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 5. API Documentation
Interactive API docs are available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Usage Example

### Endpoint
`GET /analyze/{sector}`

### Request
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/analyze/pharmaceuticals' \
  -H 'accept: application/json' \
  -H 'X-API-Key: your_secret_api_key_here'
```

### Response
The API directly returns a readable `.md` (Markdown) file formatted report:
```markdown
# Market Analysis Report: Pharmaceuticals Sector (India)

## Executive Summary
...
```

## Security
- **Authentication**: Requires a valid `X-API-Key` header matching your configured `API_KEY`. Defaults to a guest pass if none is given, but recommend strictly passing the header.
- **Rate Limiting**: Limited to 5 requests per minute per IP address.
- **Input Validation**: Sector names must be alphanumeric and between 2 to 50 characters.
