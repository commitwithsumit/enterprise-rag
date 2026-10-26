from app.retrieval.models import RetrievalResult


def build_citations(
    results: list[RetrievalResult],
) -> list[dict]:

    citations = []

    for index, result in enumerate(
        results,
        start=1
    ):

        citations.append({
            "citation_id": index,
            "source_type": result.source_type,
            "source": result.source_id,
        })

    return citations