# 🚀 InsightFlow

**AI-Powered Company Research & Insights Platform**

InsightFlow is a modern SaaS application that leverages autonomous AI agents to gather, analyze, and synthesize comprehensive company research from multiple sources in real-time. Built with React and FastAPI, it features a stunning premium UI and powerful RAG (Retrieval-Augmented Generation) capabilities.

![InsightFlow](https://img.shields.io/badge/Status-Production%20Ready-success)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

- 🤖 **Autonomous AI Research** - Multi-agent workflow automatically collects data from web, news, Reddit, GitHub
- 💬 **Intelligent Chat Interface** - Ask questions about researched companies using natural language
- 📊 **Interactive Visualizations** - Beautiful charts and stats showing data sources and insights
- 🎨 **Premium UI/UX** - Modern glassmorphism design with smooth animations
- 🔄 **Real-time Processing** - Live updates during research workflow
- 🐳 **Docker Ready** - Complete Docker Compose setup with all services
- 🚀 **Deploy Anywhere** - Backend containerized, frontend as static site

## 🏗️ Architecture

```
├── backend/              # FastAPI backend with AI agents
│   ├── app.py           # Main API application
│   ├── agents.py        # Autonomous research agents
│   ├── helper.py        # Utility functions
│   ├── config.py        # Configuration
│   ├── services/        # Business logic services
│   └── Dockerfile       # Backend Docker image
│
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── App.jsx      # Main application
│   └── package.json
│
└── docker-compose.yml   # Complete stack orchestration
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### 1. Clone & Setup

```bash
git clone <your-repo>
cd InsightFlow

# Copy environment file
cp .env.example .env

# Add your Gemini API key to .env
# GEMINI_API_KEY=your_api_key_here
```

### 2. Start Services with Docker

```bash
# Start all services (Milvus, etcd, MinIO, Backend)
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f backend
```

Services will be available at:
- **Backend API**: http://localhost:8001
- **Milvus**: localhost:19530
- **MinIO Console**: http://localhost:9001

### 3. Start Frontend (Development)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend will be available at: http://localhost:5173

## 📦 Deployment

### Backend Deployment (Render/Railway/Fly.io)

The backend is fully containerized:

1. **Dockerfile** is production-ready with multi-stage build
2. Set environment variables:
   ```
   GEMINI_API_KEY=your_key
   MILVUS_HOST=your_milvus_host
   MILVUS_PORT=19530
   ```
3. Deploy the `backend/` directory

### Frontend Deployment (Vercel/Netlify/Render Static)

The frontend builds to static files:

```bash
cd frontend
npm run build
# Deploy the 'dist/' folder
```

Set build command: `npm run build`
Set publish directory: `dist`

Add environment variable:
```
VITE_API_URL=https://your-backend-url.com
```

## 🔧 Configuration

### Backend Environment Variables

```env
# Required
GEMINI_API_KEY=your_gemini_api_key

# Milvus Configuration
MILVUS_HOST=localhost  # or your Milvus service URL
MILVUS_PORT=19530
COLLECTION_NAME=insightflow_docs

# CORS
FRONTEND_URL=http://localhost:5173
```

### Frontend Environment Variables

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8001  # Your backend URL
```

## 🎯 Usage

1. **Research a Company**
   - Navigate to http://localhost:5173
   - Enter a company name (e.g., "OpenAI", "Tesla", "Microsoft")
   - Click "Start Research"
   - Watch as AI agents collect and analyze data

2. **Explore Insights**
   - View the auto-generated summary
   - See data source breakdown in charts
   - Check collection statistics

3. **Chat with Research**
   - Ask questions about the company
   - Get instant AI-powered answers from the research data
   - Use suggested questions or ask your own

## 📡 API Endpoints

### Research
```http
POST /research/
{
  "company_name": "OpenAI"
}
```

### Chat
```http
POST /chat/
{
  "company_name": "OpenAI",
  "prompt": "What are their main products?"
}
```

### List Companies
```http
GET /companies/
```

### Health Check
```http
GET /health
```

## 🛠️ Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app:app --reload --port 8001
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start dev server with hot reload
npm run dev

# Build for production
npm run build
```

## 🎨 Tech Stack

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Recharts
- Axios
- React Icons

**Backend:**
- FastAPI
- LlamaIndex
- Google Gemini
- LangGraph
- DuckDuckGo Search API

**Database & Infrastructure:**
- Milvus (Vector Database)
- MinIO (Object Storage)
- etcd (Metadata Store)
- Docker & Docker Compose

## 📝 Project Structure Details

### Key Backend Files

- `agents.py` - Multi-agent research workflow (Search → Plan → Fetch → Clean → Store → Summarize)
- `app.py` - FastAPI application with REST endpoints
- `helper.py` - Gemini LLM setup, embeddings, vector store utilities
- `services/ingestion.py` - Vector index management
- `services/chat_service.py` - RAG chat engine configuration

### Key Frontend Components

- `App.jsx` - Main router and state management
- `ResearchForm.jsx` - Company research input with loading states
- `Visualization.jsx` - Charts and stats display
- `ChatInterface.jsx` - Interactive RAG chat with message history

## 🧹 Cleanup

Previous `Project/` folder with streamlit/chainlit has been removed. This is a clean restructure with only essential files.

## 📄 License

MIT License - feel free to use this for your projects!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open a GitHub issue.

---

