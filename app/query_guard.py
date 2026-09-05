import re


def validate_question(question):
    """
    Check whether the user's question is asking for a
    read-only operation.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    forbidden_words = [
        "delete",
        "update",
        "insert",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "modify",
        "change",
        "set",
    ]

    for word in forbidden_words:
        pattern = rf"\b{word}\b"

        if re.search(pattern, question, re.IGNORECASE):
            raise ValueError(
                "Only read-only questions are allowed."
            )

    return question.strip()