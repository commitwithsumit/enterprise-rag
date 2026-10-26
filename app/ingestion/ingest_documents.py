from pathlib import Path

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.splitter import split_documents
from app.ingestion.resource_metadata import load_resource_metadata
from app.ingestion.vector_store import create_vector_store
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


from dotenv import load_dotenv
load_dotenv()


BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "enterprise"
    / "documents"
)


def find_resource_metadata(
    pdf_path: Path,
    resource_metadata: dict,
):
    target_path = pdf_path.resolve()

    for metadata in resource_metadata.values():
        relative_path = metadata.get("path", "").strip()

        if not relative_path:
            continue

        metadata_path = (
            PROJECT_ROOT / relative_path
        ).resolve()

        if metadata_path == target_path:
            return metadata

    return None


def ingest_documents():

    resource_metadata = load_resource_metadata()

    all_documents = []

    pdf_files = list(
        BASE_PATH.rglob("*.pdf")
    )

    print("PDF files found:", len(pdf_files))

    for pdf_path in pdf_files:

        print("\nProcessing:", pdf_path)

        documents = load_pdf(
            str(pdf_path)
        )

        metadata = find_resource_metadata(
            pdf_path,
            resource_metadata,
        )

        if metadata is None:

            print(
                "WARNING: No resource metadata found"
            )

            continue

        print(
            "Resource ID:",
            metadata["resource_id"]
        )

        print(
            "Classification:",
            metadata["classification"]
        )

        print(
            "Department:",
            metadata["department"]
        )

        # Attach metadata BEFORE chunking
        for document in documents:

            document.metadata.update({
                "resource_id": metadata["resource_id"],
                "classification": metadata["classification"],
                "department_id": metadata["department"],
            })

        all_documents.extend(documents)

    print(
        "\nLoaded documents:",
        len(all_documents)
    )

    # Split after metadata has been attached
    chunks = split_documents(
        all_documents
    )

    print(
        "Total chunks:",
        len(chunks)
    )

    vector_store = create_vector_store(
        chunks
    )

    print(
        "\nVector store created successfully!"
    )

    return vector_store


if __name__ == "__main__":

    ingest_documents()
