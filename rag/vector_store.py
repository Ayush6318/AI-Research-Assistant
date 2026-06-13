from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embedding_model
import os

def create_vector_store(chunks, index_name="default"):

    embeddings = get_embedding_model()

    vector_store = FAISS.from_documents(chunks, embeddings)

   
    save_path = f"faiss_index/{index_name}"
    os.makedirs(save_path, exist_ok=True)

    vector_store.save_local(save_path)
    
    return vector_store

def load_vector_store(index_name="default"):
  
    embeddings = get_embedding_model()

    load_path = f"faiss_index/{index_name}"

    if not os.path.exists(load_path):
        return None

    vector_store = FAISS.load_local(
        folder_path=load_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store