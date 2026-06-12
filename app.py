from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from agents.research_agent import get_research_chain

from agents.coding_agent import get_coding_chain

from agents.summary_agent import get_summary_chain

from agents.router import get_router_chain

from agents.router import classify_query

from utils.memory import format_history

from database import save_message
from database import get_messages

from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message":"AI Research Assistant is running"
    }

class QueryRequest(BaseModel):
    query:str
    session_id:str

import os

# Load environment variables
load_dotenv()

# LangSmith Configuration
os.environ["LANGSMITH_PROJECT"] = "AI_RESEARCH_ASSISTANT"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_TRACING"] = "true"

llm = ChatGoogleGenerativeAI(
  model = 'gemini-2.5-flash'
)


research_chain = get_research_chain(llm)
coding_chain = get_coding_chain(llm)
summary_chain = get_summary_chain(llm)
router_chain = get_router_chain(llm)


@app.post("/chat")
def chat(request: QueryRequest):

    query = request.query

    save_message(request.session_id,
                 "user",
                 query)
    
    history = get_messages(
        request.session_id
    )[-10:]

    conversation_histroy = format_history(
        history
    )

    enhanced_query = f"""
previous conversation:
{conversation_histroy}
current user question:
{query}
"""

    route = classify_query(
        router_chain,
        query
    )

    if route == "coding":

        response = coding_chain.invoke(
            {
                "question": enhanced_query
            }
        )

    elif route == "summary":

        response = summary_chain.invoke(
            {
                "question": enhanced_query
            }
        )

    else:

        response = research_chain.invoke(
            {
                "question": enhanced_query
            }
        )

    save_message(
    request.session_id,
    "assistant",
    response.content
)

    history = get_messages(
    request.session_id
)
    
    return {

    "route": route,

    "answer": response.content,

    "history": history
}