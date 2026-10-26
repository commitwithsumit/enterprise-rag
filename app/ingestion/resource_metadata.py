import csv
from pathlib import Path


BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "enterprise"
)


def load_resource_metadata():

    file_path = (
        BASE_PATH / "resource_metadata.csv"
    )

    metadata = {}

    with file_path.open(
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            metadata[
                row["resource_id"]
            ] = row

    return metadata

if __name__ == "__main__":

    load_resource_metadata()