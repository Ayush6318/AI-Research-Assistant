def format_history(messages):

    conversation = ""

    for role, content in messages:

        conversation += (
            f"{role}: {content}\n"
        )

    return conversation