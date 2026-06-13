from rag.vector_store import load_vector_store
from rag.retriever import get_retriever

def retrieve_context(question, index_name="default"):
  
    vector_store = load_vector_store(index_name=index_name)
    
    if not vector_store:
        return ""

    retriever = get_retriever(vector_store)
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    return context

def retrieve_context_with_score(question, k=3, index_name="default"):
   
    vector_store = load_vector_store(index_name=index_name)

    if not vector_store:
        return []

    results = vector_store.similarity_search_with_score(
        question,
        k=k
    )
    return results