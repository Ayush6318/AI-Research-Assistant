from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents):

  splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 200)

  chunks = splitter.split_documents(documents=documents)

  return chunks

