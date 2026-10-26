
from app.generation.context_builder import build_context
from app.generation.prompt import build_prompt
from app.generation.llm import get_llm
from app.generation.citations import build_citations

from dotenv import load_dotenv

load_dotenv()


def calculate_confidence(results: list) -> str:
    result_count = len(results)

    if result_count >= 5:
        return "HIGH"
    if result_count >= 2:
        return "MEDIUM"
    if result_count == 1:
        return "LOW"

    return "NONE"


def generate_answer(
    query: str,
    results: list,
    authorized_resource_ids: set[str],
):
    if not results:
        return {
            "answer": (
                "I don't have enough authorized "
                "information to answer this question."
            ),
            "citations": [],
            "confidence": "NONE",
        }

    # Validate all results before creating the prompt
    # or invoking the LLM.
    context = build_context(
        results,
        authorized_resource_ids,
    )

    prompt = build_prompt(query, context)

    llm = get_llm()
    response = llm.invoke(prompt)

    citations = build_citations(results)
    confidence = calculate_confidence(results)

    return {
        "answer": response.content,
        "citations": citations,
        "confidence": confidence,
    }
