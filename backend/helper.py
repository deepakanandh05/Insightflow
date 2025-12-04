import re
import unicodedata
from pymilvus import connections
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.llms.gemini import Gemini
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import PromptTemplate
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import StorageContext


def clean_text(s: str) -> str:
    """Normalize and clean document text."""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"Page\s*\d+(\s*of\s*\d+)?", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def get_embedding_model():
    """Return embedding model compatible with LlamaIndex."""
    model_name = "BAAI/bge-small-en-v1.5"
    return HuggingFaceEmbedding(model_name=model_name)

def setup_parser(embed_model):
    """Initialize the semantic splitter node parser."""
    return SemanticSplitterNodeParser(
        buffer_size=3,
        breakpoint_percentile_threshold=95,
        embed_model=embed_model,
    )

def connect_milvus(host: str = "localhost", port: str = "19530"):
    """Connect to Milvus vector database."""
    connections.connect(alias="default", host=host, port=port)
    print(f"Connected to Milvus at {host}:{port}")

def get_vector_store(host: str, port: str, collection_name: str, token: str = None):
    """Return Milvus vector store and storage context.
    Supports both local Milvus and Zilliz Cloud."""
    
    # Determine if using Zilliz Cloud (has token) or local Milvus
    if token:
        # Zilliz Cloud configuration
        uri = f"https://{host}:{port}"
        vector_store = MilvusVectorStore(
            uri=uri,
            token=token,
            collection_name=collection_name,
            dim=384,
            overwrite=False,
        )
    else:
        # Local Milvus configuration
        uri = f"tcp://{host}:{port}"
        vector_store = MilvusVectorStore(
            uri=uri,
            collection_name=collection_name,
            dim=384,
            overwrite=False,
            index_params={
                "metric_type": "COSINE",
                "index_type": "HNSW",
                "params": {"M": 16, "efConstruction": 128},
            },
            search_params={"ef": 64},
        )
    
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return vector_store, storage_context

def setup_llm(api_key: str):
    """Initialize Gemini LLM."""
    return Gemini(
        api_key=api_key,
        model="gemini-2.5-flash",
        temperature=0.4,
    )

def setup_chat_memory(user_key: str = "user1"):
    """Initialize chat memory buffer and store."""
    chat_store = SimpleChatStore()
    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000,
        chat_store=chat_store,
        chat_store_key=user_key
    )
    return chat_store, chat_memory

def get_context_prompt():
    """Enhanced contextual prompt for market research and summarization."""
    return PromptTemplate(
        """
You are an intelligent market research AI assistant. 
Your goal is to provide clear, human-like, and insightful summaries from the retrieved context.

Guidelines:
- Always focus on the **company** mentioned in the conversation.
- Use the retrieved context to summarize **news, updates, or insights** — not metadata.
- Do **not** repeat URLs, document IDs, or raw data structures.
- Merge related facts into smooth, coherent paragraphs.
- Write in a professional and conversational tone.
- If no relevant context exists, say: "I couldn't find any recent updates for this company."

Use this structure in your answer:
1️⃣ Short intro sentence about what was found.
2️⃣ Bullet-style or paragraph summary of key insights.
3️⃣ Optional concluding insight (e.g., "This indicates strong momentum in the company's strategy.")

-----------------
Context:
{context_str}

Chat History:
{chat_history}

User Question:
{query_str}
"""
    )
