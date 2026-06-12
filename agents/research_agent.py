from langchain_core.prompts import ChatPromptTemplate

def get_research_chain(llm):

    prompt = ChatPromptTemplate.from_template(
    """
    You are an expert AI Research Assistant.

    Question:
    {question}

    Provide:

    1. Introduction
    2. Detailed Explanation
    3. Real World Applications
    4. Summary
    """
    )

    return prompt | llm