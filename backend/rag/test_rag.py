from backend.rag.retriever import search_knowledge_base


print("========================================")
print("TESTING RESTAURANT KNOWLEDGE BASE")
print("========================================")


query = "Can I cancel my order?"


result = search_knowledge_base(query)


print("\nQuery:")
print(query)


print("\nRetrieved Information:")

for item in result["results"]:
    print("----------------------------------------")
    print(item["content"])