"""
Autonomous Market Research System for InsightFlow
AI-powered company research using multi-agent workflow

Flow:
1. Search Agent → DuckDuckGo search for company info
2. Planner Agent → Decides what data to collect
3. Fetcher Agent → Gets real-time data from free APIs
4. Cleaner Agent → Cleans and creates documents
5. Storage Agent → Stores in Milvus vector DB
6. Summary Agent → Final insights with visualization
"""

import json
import re
import requests
from typing import TypedDict, List, Dict
from datetime import datetime
from duckduckgo_search import DDGS
from langgraph.graph import StateGraph, END
from llama_index.core import Document
import unicodedata
from helper import (
    connect_milvus,
    get_embedding_model,
    setup_parser,
    get_vector_store,
    setup_llm,
    setup_chat_memory,
    get_context_prompt,
)
from services.ingestion import create_or_load_vector_index
from services.chat_service import setup_chat_engine
from config import (
    MILVUS_HOST,
    MILVUS_PORT,
    COLLECTION_NAME,
    GEMINI_API_KEY,
)


# === INIT ===
llm = setup_llm(GEMINI_API_KEY)
chat_store, chat_memory = setup_chat_memory()
context_prompt = get_context_prompt()

# Caches
vector_indices = {}  
chat_engines = {}   

# ============================================================================
# STATE
# ============================================================================

class ResearchState(TypedDict):
    company_name: str
    search_results: List[Dict]
    plan: Dict
    raw_data: List[Dict]
    cleaned_documents: List[Document]
    storage_status: str
    vector_index: object
    final_summary: str
    viz_data: Dict

# ============================================================================
# AGENT 1: SEARCH (DuckDuckGo)
# ============================================================================

def search_agent(state: ResearchState) -> ResearchState:
    """Search DuckDuckGo for company information"""
    company = state["company_name"]
    print(f"\n[1. SEARCH] Searching for: {company}")
    
    results = []
    try:
        with DDGS() as ddgs:
            # Search for company info
            for result in ddgs.text(f"{company} company news products", max_results=25):
                results.append({
                    "title": result.get("title", ""),
                    "body": result.get("body", ""),
                    "url": result.get("href", ""),
                    "source": "duckduckgo"
                })
            
            # Search for recent news
            for result in ddgs.text(f"{company} latest news", max_results=25):
                results.append({
                    "title": result.get("title", ""),
                    "body": result.get("body", ""),
                    "url": result.get("href", ""),
                    "source": "duckduckgo_news"
                })
    except Exception as e:
        print(f"   ✗ Search failed: {e}")
        results = [{
            "title": f"About {company}",
            "body": f"Information about {company} company and its activities.",
            "url": "",
            "source": "fallback"
        }]
    
    state["search_results"] = results
    print(f"   ✓ Found {len(results)} results")
    return state

# ============================================================================
# AGENT 2: PLANNER (Decides what to collect)
# ============================================================================

def planner_agent(state: ResearchState, llm) -> ResearchState:
    """Decide what additional data to collect"""
    company = state["company_name"]
    search_summary = "\n".join([r["title"] for r in state["search_results"][:3]])
    
    print(f"\n[2. PLANNER] Planning data collection...")
    
    prompt = f"""Based on these search results about {company}:
{search_summary}

What additional data should we collect? Choose 2-3 from:
- reddit: Reddit discussions
- github: GitHub repositories  
- news: News articles

Output JSON only:
{{"data_sources": ["reddit", "news"], "keywords": ["keyword1", "keyword2"]}}"""
    
    try:
        response = llm.complete(prompt)
        plan = json.loads(response.text)
    except:
        plan = {
            "data_sources": ["reddit", "news"],
            "keywords": [company, f"{company} technology"]
        }
    
    state["plan"] = plan
    print(f"   ✓ Plan: {plan['data_sources']}")
    return state

# ============================================================================
# AGENT 3: FETCHER (Gets real-time data from FREE APIs)
# ============================================================================

def fetcher_agent(state: ResearchState) -> ResearchState:
    """Fetch real-time data from free sources"""
    company = state["company_name"]
    plan = state["plan"]
    
    print(f"\n[3. FETCHER] Collecting real-time data...")
    
    raw_data = []
    
    # Add search results
    raw_data.extend(state["search_results"])
    
    # Reddit (via DuckDuckGo)
    if "reddit" in plan.get("data_sources", []):
        try:
            with DDGS() as ddgs:
                for result in ddgs.text(f"{company} site:reddit.com", max_results=3):
                    raw_data.append({
                        "title": result.get("title", ""),
                        "body": result.get("body", ""),
                        "url": result.get("href", ""),
                        "source": "reddit"
                    })
            print(f"   ✓ Reddit: {len([r for r in raw_data if r['source'] == 'reddit'])} posts")
        except:
            print(f"   ✗ Reddit fetch failed")
    
    # GitHub (via DuckDuckGo)
    if "github" in plan.get("data_sources", []):
        try:
            with DDGS() as ddgs:
                for result in ddgs.text(f"{company} site:github.com", max_results=3):
                    raw_data.append({
                        "title": result.get("title", ""),
                        "body": result.get("body", ""),
                        "url": result.get("href", ""),
                        "source": "github"
                    })
            print(f"   ✓ GitHub: {len([r for r in raw_data if r['source'] == 'github'])} repos")
        except:
            print(f"   ✗ GitHub fetch failed")
    
    # Additional news
    if "news" in plan.get("data_sources", []):
        try:
            with DDGS() as ddgs:
                for result in ddgs.news(f"{company}", max_results=5):
                    raw_data.append({
                        "title": result.get("title", ""),
                        "body": result.get("body", ""),
                        "url": result.get("url", ""),
                        "source": "news",
                        "date": result.get("date", "")
                    })
            print(f"   ✓ News: {len([r for r in raw_data if r['source'] == 'news'])} articles")
        except:
            print(f"   ✗ News fetch failed")
    
    state["raw_data"] = raw_data
    print(f"   ✓ Total data points: {len(raw_data)}")
    return state

# ============================================================================
# AGENT 4: CLEANER (Cleans and creates documents)
# ============================================================================

def clean_text(text: str) -> str:
    """Clean text data"""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s\.,!?-]', '', text)
    return text

def cleaner_agent(state: ResearchState) -> ResearchState:
    """Clean data and create LlamaIndex documents"""
    print(f"\n[4. CLEANER] Cleaning and structuring data...")
    
    documents = []
    
    for idx, item in enumerate(state["raw_data"]):
        # Clean title and body
        title = clean_text(item.get("title", ""))
        body = clean_text(item.get("body", ""))
        
        if not body:
            continue
        
        # Create document
        doc_text = f"Title: {title}\n\nContent: {body}"
        
        doc = Document(
            text=doc_text,
            metadata={
                "company": state["company_name"],
                "source": item.get("source", "unknown"),
                "url": item.get("url", ""),
                "date": item.get("date", datetime.now().isoformat()),
                "doc_id": f"{state['company_name']}_{idx}"
            }
        )
        documents.append(doc)
    
    state["cleaned_documents"] = documents
    print(f"   ✓ Created {len(documents)} clean documents")
    return state

# ============================================================================
# AGENT 5: STORAGE (Store in Milvus vector DB)
# ============================================================================

def storage_agent(state: ResearchState) -> ResearchState:
    """Store documents in Milvus vector database"""
    print(f"\n[5. STORAGE] Storing in vector database...")
    
    try:
        # Connect to Milvus
        connect_milvus(MILVUS_HOST, MILVUS_PORT)
        
        # Setup embedding model
        embed_model = get_embedding_model()
        
        # Setup vector store and storage context
        vector_store, storage_context = get_vector_store(MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME)
        
        parser = setup_parser(embed_model)
        
        nodes = parser.get_nodes_from_documents(documents=state["cleaned_documents"])
        
        company = state["company_name"]
        # Create/update index
        vector_index = create_or_load_vector_index(embed_model, parser, storage_context, vector_store, nodes, COLLECTION_NAME, company)
        
        state["storage_status"] = f"✓ Stored {len(nodes)} nodes in Milvus"
        state["vector_index"] = vector_index
        print(f"   {state['storage_status']}")
        
    except Exception as e:
        state["storage_status"] = f"✗ Storage failed: {str(e)}"
        print(f"   {state['storage_status']}")
    
    return state

# ============================================================================
# AGENT 6: SUMMARY (Final insights with visualization)
# ============================================================================

def summary_agent(state: ResearchState, llm) -> ResearchState:
    """Generate concise research summary and structured visualization data"""
    print(f"\n[6. SUMMARY] Generating final report...")
    
    company = state["company_name"]
    total_sources = len(state["raw_data"])
    sources_breakdown = {}

    # Count occurrences per data source
    for item in state["raw_data"]:
        source = item.get("source", "unknown")
        sources_breakdown[source] = sources_breakdown.get(source, 0) + 1

    # Sample insights
    data_summary = "\n".join([
        f"- {item['title'][:100]}" 
        for item in state["raw_data"][:5]
    ])

    # Prompt for LLM-generated summary
    prompt = f"""Create a concise market research summary for {company}.

    Data collected from {total_sources} sources:
    {sources_breakdown}

    Sample insights:
    {data_summary}

    Create a summary with:
    1. Company Overview (2-3 sentences)
    2. Key Findings (3-4 bullet points)
    3. Market Sentiment (positive/neutral/negative with reasoning)
    4. Recommendation (1-2 sentences)

    Keep it professional but easy to understand.
    """

    try:
        response = llm.complete(prompt)
        summary_text = response.text
    except Exception:
        summary_text = f"Research completed for {company} with {total_sources} data points collected."

    # Prepare structured data for visualization
    viz_data = {
        "company_name": company,
        "total_sources": total_sources,
        "sources_breakdown": sources_breakdown,
        "summary": summary_text,
    }

    # Store in state
    state["final_summary"] = summary_text
    state["viz_data"] = viz_data

    print(f"✓ Visualization data ready for {company}")
    return state

# ============================================================================
# WORKFLOW
# ============================================================================

def build_workflow(llm) -> StateGraph:
    """Build simple linear workflow"""
    
    workflow = StateGraph(ResearchState)
    
    # Add all agents
    workflow.add_node("search", search_agent)
    workflow.add_node("planner", lambda s: planner_agent(s, llm))
    workflow.add_node("fetcher", fetcher_agent)
    workflow.add_node("cleaner", cleaner_agent)
    workflow.add_node("storage", storage_agent)
    workflow.add_node("summary", lambda s: summary_agent(s, llm))
    
    workflow.add_edge("search", "planner")
    workflow.add_edge("planner", "fetcher")
    workflow.add_edge("fetcher", "cleaner")
    workflow.add_edge("cleaner", "storage")
    workflow.add_edge("storage", "summary")
    workflow.add_edge("summary", END)
    
    workflow.set_entry_point("search")

    final_workflow = workflow.compile()
    
    return final_workflow

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def research_company(company_name: str):
    """Run autonomous research for a company"""
    # Build workflow
    app = build_workflow(llm)
    
    # Initial state
    initial_state = {
        "company_name": company_name,
        "search_results": [],
        "plan": {},
        "raw_data": [],
        "cleaned_documents": [],
        "storage_status": "",
        "vector_index": None,
        "final_summary": "",
        "viz_data": ""
    }
    
    # Run!
    final_state = app.invoke(initial_state)
    vector_index = final_state.get("vector_index", None)
    return final_state, vector_index

def research_company_cached(company_name: str):
    """Run research only once per company, cache result."""
    if company_name in vector_indices:
        return vector_indices[company_name], vector_indices[company_name]["vector_index"]
    
    final_state, vector_index = research_company(company_name)
    vector_indices[company_name] = final_state
    return final_state, vector_index

def get_chat_engine(company_name: str):
    """Get chat engine for a company, create if missing."""
    if company_name in chat_engines:
        return chat_engines[company_name]
    
    final_state, vector_index = research_company_cached(company_name)
    chat_bot = setup_chat_engine(vector_index, llm, chat_memory, context_prompt, company_name)
    chat_engines[company_name] = chat_bot

    return chat_bot
