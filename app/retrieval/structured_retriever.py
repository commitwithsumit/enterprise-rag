import csv
import re
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


STRUCTURED_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "enterprise"
    / "structured"
)


def search_structured_data(
    query: str,
    file_name: str | None = None,
    allowed_resource_ids: set[str] | None = None,
) -> list[RetrievalResult]:

    normalized_query = query.lower()

    # Identify quarter from the query
    quarter_match = re.search(
        r"\bq[1-4]\b",
        normalized_query
    )

    requested_quarter = None

    if quarter_match:
        requested_quarter = quarter_match.group(0).upper()

    print("Requested quarter:", requested_quarter)

    # Decide which files to search
    if file_name:
        files = [STRUCTURED_PATH / file_name]
    else:
        files = list(STRUCTURED_PATH.glob("*.csv"))

    results = []

    for file_path in files:

        if not file_path.exists():
            continue

        resource_id = get_resource_id_for_file(file_path)

        # Fail closed: don't search a file without a resource mapping.
        if resource_id is None:
            print("WARNING: No resource mapping for", file_path.name)
            continue

        if (
                allowed_resource_ids is not None
                and resource_id not in allowed_resource_ids
        ):
            continue

        with file_path.open(
                newline="",
                encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                # Special handling for financial records
                if (
                    file_path.name == "financial_records.csv"
                    and requested_quarter
                ):

                    row_quarter = row.get(
                        "quarter",
                        ""
                    ).upper()

                    # Convert Q3-2026 → Q3
                    row_quarter_prefix = row_quarter.split("-")[0]

                    if row_quarter_prefix != requested_quarter:
                        continue

                    results.append(
                        RetrievalResult(
                            source_type="STRUCTURED",
                            source_id=file_path.name,
                            content=str(row),
                            metadata={
                                "file": file_path.name,
                                "resource_id": resource_id,
                                "quarter": row_quarter,
                            }
                        )
                    )

                    continue

                # Generic fallback matching
                row_text = " ".join(
                    str(value)
                    for value in row.values()
                ).lower()

                query_words = normalized_query.split()

                matched = any(
                    word in row_text
                    for word in query_words
                    if len(word) > 2
                )

                if matched:

                    results.append(
                        RetrievalResult(
                            source_type="STRUCTURED",
                            source_id=file_path.name,
                            content=str(row),
                            metadata={
                                "file": file_path.name,
                                "resource_id": resource_id,
                            }
                        )
                    )

    return results