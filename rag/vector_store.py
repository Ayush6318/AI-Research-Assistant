from langchain_classic.vectorstores import FAISS

from rag.embeddings import get_embedding_model

def create_vector_store(chunks):

  embeddings = get_embedding_model()

  vector_store = FAISS.from_documents(
    chunks , embeddings
  )

  vector_store.save_local("faiss_index")

  return vector_store

def load_vector_store():
  embeddings  = get_embedding_model()

  vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
  )

  return vector_store