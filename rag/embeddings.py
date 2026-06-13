from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

def get_embedding_model():

  return GoogleGenerativeAIEmbeddings(

   model="models/gemini-embedding-2"

)

