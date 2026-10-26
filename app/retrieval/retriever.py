from app.query.analyzer import analyze_query
from app.query.router import route_query

from app.retrieval.models import RetrievalResult
from app.retrieval.document_retriever import search_documents
from app.retrieval.structured_retriever import search_structured_data
from app.retrieval.json_retriever import search_json_logs


def retrieve(
    query: str,
    top_k: int = 3,
) -> list[RetrievalResult]:

    analysis = analyze_query(query)

    sources = route_query(analysis)

    all_results = []

    print("\nQuery Analysis")
    print("----------------")
    print("Query:", query)
    print("Intent:", analysis.intent)
    print("Sources:", sources)
    print("Retrieval Hints:", analysis.retrieval_hints)

    # --------------------------------
    # DOCUMENT RETRIEVAL
    # --------------------------------

    if "DOCUMENT" in sources:

        document_files = (
            analysis.retrieval_hints.get(
                "documents",
                []
            )
        )

        results = search_documents(
            query,
            k=top_k,
        )

        if document_files:

            results = [
                result
                for result in results
                if any(
                    file_name in result.source_id
                    for file_name in document_files
                )
            ]

        all_results.extend(results)

    # --------------------------------
    # STRUCTURED RETRIEVAL
    # --------------------------------

    if "STRUCTURED" in sources:

        structured_files = (
            analysis.retrieval_hints.get(
                "structured",
                []
            )
        )

        if structured_files:

            for file_name in structured_files:

                results = search_structured_data(
                    query,
                    file_name=file_name,
                )

                all_results.extend(
                    results[:top_k]
                )

        else:

            results = search_structured_data(
                query
            )

            all_results.extend(
                results[:top_k]
            )

    # --------------------------------
    # JSON LOG RETRIEVAL
    # --------------------------------

    if "JSON_LOG" in sources:

        json_files = (
            analysis.retrieval_hints.get(
                "json_logs",
                []
            )
        )

        if json_files:

            for file_name in json_files:

                results = search_json_logs(
                    query,
                    file_name=file_name,
                )

                all_results.extend(
                    results[:top_k]
                )

        else:

            results = search_json_logs(
                query
            )

            all_results.extend(
                results[:top_k]
            )

    # --------------------------------
    # FINAL RESULTS
    # --------------------------------

    return all_results