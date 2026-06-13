

from dotenv import load_dotenv
import os

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI

from agents.research_agent import get_research_chain
from agents.coding_agent import get_coding_chain
from agents.summary_agent import get_summary_chain
from agents.router import get_router_chain, classify_query

from utils.memory import format_history
from database import save_message, get_messages

from rag.pdf_loader import load_pdf
from rag.text_splitter import split_documents
from rag.vector_store import create_vector_store
from rag.rag_answer import retrieve_context_with_score 
from rag.rag_chain import get_rag_chain

app = FastAPI()

load_dotenv()

os.environ["LANGSMITH_PROJECT"] = "AI_RESEARCH_ASSISTANT"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_TRACING"] = "true"

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

rag_chain = get_rag_chain(llm)
research_chain = get_research_chain(llm)
coding_chain = get_coding_chain(llm)
summary_chain = get_summary_chain(llm)
router_chain = get_router_chain(llm)

class QueryRequest(BaseModel):
    query: str
    session_id: str

@app.get("/")
def home():
    return {"message": "AI Research Assistant is running"}


import os
import uuid

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):

    try:
        os.makedirs("uploads", exist_ok=True)

        filename = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join("uploads", filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        docs = load_pdf(file_path)

        chunks = split_documents(docs)

        create_vector_store(chunks)

        return {
            "message": "PDF uploaded successfully",
            "chunks": len(chunks)
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/chat")
def chat(request: QueryRequest):

    query = request.query

    
    save_message(request.session_id, "user", query)

   
    history = get_messages(request.session_id)[-10:]
    conversation_history = format_history(history)

    enhanced_query = f"""
Previous conversation:
{conversation_history}

Current user question:
{query}
"""

    try:
        results = retrieve_context_with_score(query, k=3)
        # format: [(doc, score), ...]
    except Exception:
        results = []

    #  Decide RAG vs Agents using SCORE
 
    USE_RAG_THRESHOLD = 0.75  # tune later

    use_rag = False
    context = ""

    if results and len(results) > 0:

        best_doc, best_score = results[0]

        # FAISS: lower score = better match
        if best_score < USE_RAG_THRESHOLD:
            use_rag = True
            context = "\n\n".join([doc.page_content for doc, _ in results])

 
    route = classify_query(router_chain, query)

    if use_rag:
        response = rag_chain.invoke({
            "context": context,
            "question": query
        })

        final_route = "rag"

    else:
        if route == "coding":
            response = coding_chain.invoke({
                "question": enhanced_query
            })

        elif route == "summary":
            response = summary_chain.invoke({
                "question": enhanced_query
            })

        else:
            response = research_chain.invoke({
                "question": enhanced_query
            })

        final_route = route

  
    answer = getattr(response, "content", response)

    save_message(request.session_id, "assistant", answer)

    history = get_messages(request.session_id)

    return {
        "route": final_route,
        "answer": answer,
        "history": history
    }