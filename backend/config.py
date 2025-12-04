import os
from dotenv import load_dotenv

load_dotenv()

# Milvus Configuration
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
MILVUS_TOKEN = os.getenv("MILVUS_TOKEN", "")  # For Zilliz Cloud
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "insightflow_docs")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Frontend URL (for CORS)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Backend Configuration
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8001"))
