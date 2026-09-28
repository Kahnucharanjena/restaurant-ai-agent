from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE = BASE_DIR / "knowledge_base" / "restaurant_policies.txt"

VECTORSTORE_PATH = BASE_DIR / "rag" / "faiss_index"


# ==========================================
# LOAD DOCUMENT
# ==========================================

print("Loading knowledge base...")

loader = TextLoader(
    str(KNOWLEDGE_BASE),
    encoding="utf-8"
)

documents = loader.load()

print(f"Loaded {len(documents)} document(s)")


# ==========================================
# SPLIT DOCUMENT
# ==========================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


# ==========================================
# CREATE EMBEDDINGS
# ==========================================

print("Creating embeddings...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# CREATE FAISS VECTOR STORE
# ==========================================

print("Creating FAISS vector store...")

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


# ==========================================
# SAVE VECTOR STORE
# ==========================================

vectorstore.save_local(str(VECTORSTORE_PATH))

print("========================================")
print("RAG VECTOR STORE CREATED SUCCESSFULLY")
print("========================================")
print(f"Location: {VECTORSTORE_PATH}")