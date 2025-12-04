# InsightFlow Backend

FastAPI application with AI-powered research agents and RAG capabilities.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## Run

```bash
uvicorn app:app --reload --port 8001
```

## Docker

```bash
docker build -t insightflow-backend .
docker run -p 8001:8001 --env-file .env insightflow-backend
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
