from langchain_core.prompts import ChatPromptTemplate

def get_coding_chain(llm):

    prompt = ChatPromptTemplate.from_template(
    """
    You are a senior software engineer.

    Question:
    {question}

    Give:

    1. Explanation
    2. Clean Code
    3. Code Comments
    4. Best Practices
    """
    )

    return prompt | llm