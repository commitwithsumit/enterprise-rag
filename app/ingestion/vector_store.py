from pathlib import Path

from langchain_chroma import Chroma

from app.ingestion.embeddings import (
    get_embedding_model,
)


VECTOR_DB_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "vectorstore"
    / "chroma"
)


def create_vector_store(
    documents,
):

    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(
            VECTOR_DB_PATH
        ),
        collection_name="enterprise_documents",
    )

    return vector_store