import json
import csv
from pathlib import Path
from app.retrieval.models import RetrievalResult

RESOURCE_METADATA_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "enterprise"
    / "resource_metadata.csv"
)

def get_resource_id_for_file(file_path: Path) -> str | None:
    with RESOURCE_METADATA_PATH.open(
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            metadata_path = row.get("path", "")

            if (
                metadata_path
                and Path(metadata_path).name.lower()
                == file_path.name.lower()
            ):
                return row["resource_id"]

    return None

LOG_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "enterprise"
    / "logs"
)

def search_json_logs(
    query: str,
    file_name: str | None = None,
    allowed_resource_ids: set[str] | None = None,
) -> list[RetrievalResult]:

    normalized_query = query.lower()

    if file_name:
        files = [LOG_PATH / file_name]
    else:
        files = list(LOG_PATH.glob("*.json"))

    results = []

    for file_path in files:

        if not file_path.exists():
            continue

        resource_id = get_resource_id_for_file(file_path)

        if resource_id is None:
            print("WARNING: No resource mapping for", file_path.name)
            continue

        if (
                allowed_resource_ids is not None
                and resource_id not in allowed_resource_ids
        ):
            continue

        with file_path.open(
            encoding="utf-8"
        ) as file:

            records = json.load(file)

        for record in records:

            record_text = json.dumps(
                record
            ).lower()

            query_words = normalized_query.split()

            matched = any(
                word in record_text
                for word in query_words
                if len(word) > 2
            )

            if matched:

                results.append(
                    RetrievalResult(
                        source_type="JSON_LOG",
                        source_id=file_path.name,
                        content=json.dumps(record),
                        metadata={
                            "file": file_path.name,
                            "resource_id": resource_id,
                        }
                    )
                )

    return results