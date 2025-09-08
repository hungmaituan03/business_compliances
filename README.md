# Business Compliances Web Tool

## Live Demo
Access the deployed frontend here: [business-compliances.vercel.app](https://business-compliances.vercel.app/)

## Overview
A web application to help US business owners determine applicable rules and compliance steps for their business, including federal and state regulations. The tool uses advanced search, summarization, and retrieval-augmented generation (RAG) to provide actionable compliance guidance.

## Tech Stack
- **Backend:**
  - Python 3.13
  - Flask (API server)
  - FAISS (vector search)
  - OpenAI API (embeddings, LLM summarization)
  - Gunicorn (production WSGI server)
  - Flask-CORS (CORS support)
  - python-dotenv (environment variables)
- **Frontend:**
  - React (JavaScript/TypeScript)
  - Modern UI components
- **Deployment:**
  - Backend: Render
  - Frontend: Vercel or Netlify
- **Testing:**
  - Backend: Flask test client, Python scripts
  - Frontend: React testing library (optional)

## Setup Instructions
### Backend
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up `.env` file with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-key-here
   ```
3. Run locally:
   ```bash
   python app.py
   ```

### Frontend
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run locally:
   ```bash
   npm start
   ```

## API Documentation
### POST `/get-rules`
- **Description:** Returns relevant business rules and compliance summary for a given business profile.
- **Request Body Example:**
  ```json
  {
    "state": "CA",
    "industry": "Retail",
    "size": "1-10 employees",
    "structure": "LLC",
    "complianceFocus": ["Tax"]
  }
  ```
- **Response Example:**
  ```json
  {
    "results": [ ... ],
    "summary": "..."
  }
  ```

## How It Works

### Data Structure Visualization
The tool uses a combination of FAISS for vector search and OpenAI's embeddings to structure and retrieve data efficiently. Here's a high-level overview:

1. **Data Ingestion:**
   - Business rules and compliance data are preprocessed and embedded using OpenAI's embedding model.
   - The embeddings are stored in FAISS for fast similarity search.

2. **Query Processing:**
   - User queries are embedded in real-time and matched against the stored embeddings in FAISS.
   - Relevant rules are retrieved and summarized using OpenAI's language model.

3. **Frontend Integration:**
   - The React frontend sends user queries to the Flask backend.
   - Results are displayed in a user-friendly format, including summaries and detailed rules.

## Testing
- Run backend tests:
  ```bash
  python test_backend_api.py
  ```
- Run frontend tests (if available):
  ```bash
  cd frontend
  npm test
  ```

## Rate Limiting and Reliability
- Embedding calls are limited to 10 per minute to avoid API rate limits.
- All OpenAI API calls use strict timeouts and process isolation to prevent backend hangs.

## Contributing
- Fork the repository and submit pull requests.
- Report issues via GitHub Issues.
- Follow PEP8 and best practices for Python code.

## License
MIT License
