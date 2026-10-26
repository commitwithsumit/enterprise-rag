def evaluate_citations(
    answer: str,
    citations: list[dict],
) -> dict:

    citation_ids = {
        citation["citation_id"]
        for citation in citations
    }

    used_citations = set()

    for citation_id in citation_ids:

        marker = f"[{citation_id}]"

        if marker in answer:
            used_citations.add(citation_id)

    valid = len(used_citations)

    total = len(citation_ids)

    precision = (
        valid / total
        if total > 0
        else 0.0
    )

    return {
        "total_citations": total,
        "used_citations": valid,
        "citation_coverage": precision,
    }