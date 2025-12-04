from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents import get_chat_engine, research_company_cached, chat_engines, vector_indices
from config import FRONTEND_URL

app = FastAPI(
    title="InsightFlow API",
    description="AI-Powered Company Research and Insights Platform",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    """API root endpoint"""
    return {
        "service": "InsightFlow API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/research/")
async def research(request: Request):
    """
    Run autonomous research for a company
    ---
    Body:
        company_name: str - Name of the company to research
    
    Returns:
        response: str - Research status message
        viz_data: dict - Visualization data including summary and sources
        chat_ready: bool - Whether chat is ready for this company
    """
    data = await request.json()
    company = data.get("company_name")
    if not company:
        return {"error": "company_name is required"}
    
    final_state, vector_index = research_company_cached(company)
    return {
        "response": f"Research completed successfully for {company}.",
        "viz_data": final_state.get("viz_data"),
        "chat_ready": True
    }


@app.post("/chat/")
async def chat_endpoint(request: Request):
    """
    Chat with RAG engine for a researched company
    ---
    Body:
        company_name: str - Name of the company
        prompt: str - User query
    
    Returns:
        company_name: str - Company name
        query: str - User query
        response: str - AI response from RAG
    """
    data = await request.json()
    company = data.get("company_name", "")
    query = data.get("prompt", "")
    
    if not company or not query:
        return {"error": "company_name and prompt are required"}

    bot = get_chat_engine(company)
    response = bot.chat(query)
    return {
        "company_name": company,
        "query": query,
        "response": str(response)
    }


@app.delete("/reset/{company_name}")
async def reset_company(company_name: str):
    """
    Reset cached data for a specific company
    ---
    Path:
        company_name: str - Company to reset
    
    Returns:
        message: str - Status message
        removed: list - List of removed data types
    """
    removed = []
    if company_name in chat_engines:
        del chat_engines[company_name]
        removed.append("chat_engine")
    if company_name in vector_indices:
        del vector_indices[company_name]
        removed.append("vector_index")
    if not removed:
        return {"message": f"No cached data for {company_name}"}
    return {
        "message": f"Reset complete for {company_name}",
        "removed": removed
    }


@app.get("/companies/")
async def list_companies():
    """
    List all researched companies
    ---
    Returns:
        companies: list - List of company names
        count: int - Total number of companies
    """
    return {
        "companies": list(vector_indices.keys()),
        "count": len(vector_indices)
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    ---
    Returns:
        status: str - Health status
        active_sessions: int - Number of active chat sessions
    """
    return {
        "status": "healthy",
        "service": "InsightFlow",
        "active_sessions": len(chat_engines),
        "researched_companies": len(vector_indices)
    }


if __name__ == "__main__":
    import uvicorn
    from config import BACKEND_PORT
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
