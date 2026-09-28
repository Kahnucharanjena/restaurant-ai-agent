from backend.rag.retriever import search_knowledge_base


def search_kb(query: str):
    """
    Search the restaurant knowledge base for
    policy and FAQ information.
    """

    if not query or not query.strip():
        return {
            "success": False,
            "error": "INVALID_QUERY",
            "message": "Knowledge base query cannot be empty."
        }

    try:
        result = search_knowledge_base(query)

        return {
            "success": True,
            "query": query,
            "results": result["results"]
        }

    except Exception:
        return {
            "success": False,
            "error": "KNOWLEDGE_BASE_ERROR",
            "message": "Unable to search the knowledge base."
        }