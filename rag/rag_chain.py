from langchain_core.prompts import ChatPromptTemplate


def get_rag_chain(llm):

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful AI assistant.

        Answer ONLY from the provided context.

        Context:
        {context}

        Question:
        {question}
        """
    )

    chain = prompt | llm

    return chain