import chromadb
from chromadb.utils import embedding_functions

# Initialize Chroma client (persistent)
client = chromadb.PersistentClient(path="./chroma_db")

# Default embedding function (can be replaced with OpenAI/HuggingFace)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Create (or load) collection
collection = client.get_or_create_collection(
    name="analysis_results",
    embedding_function=embedding_fn
)

def add_analysis_result(result_id: str, query: str, analysis: str, metadata: dict):
    """Store analysis + metadata in ChromaDB"""
    collection.add(
        ids=[result_id],
        documents=[analysis],
        metadatas=[{"query": query, **metadata}]
    )

def search_similar(query: str, top_k: int = 3):
    """Semantic search in stored results"""
    return collection.query(
        query_texts=[query],
        n_results=top_k
    )
