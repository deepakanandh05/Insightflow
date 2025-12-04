from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.chat_engine import ContextChatEngine

def setup_chat_engine(vector_index, llm, chat_memory, context_prompt, company_name):
    filters = MetadataFilters(
        filters=[ExactMatchFilter(key="company", value=company_name)]
    )

    retriever = VectorIndexRetriever(
        index=vector_index,
        similarity_top_k=5,
        filters=filters,
    )

    reranker = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3
    )
    base_prompt_text = context_prompt.template if hasattr(context_prompt, "template") else str(context_prompt)

    chat_engine = ContextChatEngine.from_defaults(
        retriever=retriever,
        llm=llm,
        memory=chat_memory.get(company_name),
        system_prompt=(
            f"{base_prompt_text}\n\n"
            "Now act as a professional market research assistant.\n"
            "Summarize your findings in a clean, natural paragraph.\n"
            "Avoid showing raw metadata like URLs or doc IDs.\n"
        ),
        node_postprocessors=[reranker],
        verbose=True,
    )

    return chat_engine
