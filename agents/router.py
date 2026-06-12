from langchain_core.prompts import ChatPromptTemplate

def get_router_chain(llm):

    prompt = ChatPromptTemplate.from_template(
    """
    You are a routing agent.

    Classify the user query into exactly one category:

    research
    coding
    summary

    Rules:

    - research = explanations, concepts, theory, learning
    - coding = programming, debugging, code generation
    - summary = summarization of content

    User Query:
    {query}

    Return ONLY one word:
    research
    coding
    or
    summary
    """
    )

    return prompt | llm

def classify_query(router_chain,query):
    
    response = router_chain.invoke(
        {
            "query":query
        }
    )
    return response.content.strip().lower()