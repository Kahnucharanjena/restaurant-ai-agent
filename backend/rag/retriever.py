from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_PATH = BASE_DIR / "rag" / "faiss_index"


# ==========================================
# LOAD EMBEDDINGS
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# LOAD FAISS DATABASE
# ==========================================

vectorstore = FAISS.load_local(
    str(VECTORSTORE_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)


# ==========================================
# SEARCH KNOWLEDGE BASE
# ==========================================

def search_knowledge_base(query: str, k: int = 3):

    documents = vectorstore.similarity_search(
        query,
        k=k
    )

    results = []

    for document in documents:
        results.append({
            "content": document.page_content,
            "source": document.metadata.get("source", "knowledge_base")
        })

    return {
        "success": True,
        "query": query,
        "results": results
    }