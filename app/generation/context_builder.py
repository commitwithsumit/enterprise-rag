
from app.retrieval.models import RetrievalResult


def build_context(
    results: list[RetrievalResult],
    authorized_resource_ids: set[str],
) -> str:
    """
    Build LLM context only from authorized resources.

    Fail closed if any result has missing or unauthorized
    resource metadata.
    """

    if not authorized_resource_ids:
        if results:
            raise PermissionError(
                "Cannot build context without authorized resources."
            )
        return ""

    # Validate the entire batch before adding any content.
    for result in results:
        resource_id = result.metadata.get("resource_id")

        if not resource_id:
            raise PermissionError(
                "Retrieved result is missing resource_id metadata."
            )

        if resource_id not in authorized_resource_ids:
            raise PermissionError(
                "Retrieved result contains an unauthorized resource."
            )

    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"""
SOURCE [{index}]
Type: {result.source_type}
Source: {result.source_id}

Content:
{result.content}
"""
        )

    return "\n".join(context_parts)
