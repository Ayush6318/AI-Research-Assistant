from rag.vector_store import load_vector_store
from rag.retriever import get_retriever

def retrieve_context(question):

    vector_store = load_vector_store()

    retriever = get_retriever(vector_store)

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    return context

def retrieve_context_with_score(question, k=3):

    vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(
        question,
        k=k
    )

    return results