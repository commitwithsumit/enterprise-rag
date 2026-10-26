from pathlib import Path

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.retrieval.models import RetrievalResult


VECTOR_DB_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "vectorstore"
    / "chroma"
)


def search_documents(
    query: str,
    k: int = 3,
    allowed_resource_ids: set[str] | None = None,
) -> list[RetrievalResult]:

    # An explicitly empty set means access to no resources.
    if allowed_resource_ids is not None and not allowed_resource_ids:
        return []

    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = Chroma(
        collection_name="enterprise_documents",
        persist_directory=str(VECTOR_DB_PATH),
        embedding_function=embedding_model,
    )

    search_kwargs = {"k": k}

    if allowed_resource_ids is not None:
        search_kwargs["filter"] = {
            "resource_id": {
                "$in": list(allowed_resource_ids)
            }
        }

    results = vector_store.similarity_search_with_score(
        query,
        **search_kwargs,
    )

    return [
        RetrievalResult(
            source_type="DOCUMENT",
            source_id=document.metadata.get("source", "unknown"),
            content=document.page_content,
            metadata=document.metadata,
            score=float(score),
        )
        for document, score in results
    ]