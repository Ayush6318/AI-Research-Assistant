from langchain_core.prompts import ChatPromptTemplate

def get_summary_chain(llm):

    prompt = ChatPromptTemplate.from_template(
    """
    Summarize the following content.

    Content:
    {question}

    Provide:

    1. Key Points
    2. Short Summary
    3. Important Takeaways
    """
    )

    return prompt | llm