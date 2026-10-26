import re


def normalize_text(text: str) -> set[str]:

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )

    return {
        word
        for word in words
        if len(word) > 3
    }


def calculate_groundedness(
    answer: str,
    context: str,
) -> float:

    answer_words = normalize_text(answer)
    context_words = normalize_text(context)

    if not answer_words:
        return 0.0

    supported_words = (
        answer_words.intersection(context_words)
    )

    return len(supported_words) / len(answer_words)