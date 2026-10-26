import csv
from pathlib import Path

from app.models.resource import Resource


class ResourceRepository:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get_by_id(self, resource_id: str) -> Resource | None:

        with self.file_path.open(
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["resource_id"] == resource_id:
                    return Resource(
                        resource_id=row["resource_id"],
                        resource_name=row["resource_name"],
                        resource_type=row["resource_type"],
                        classification=row["classification"],
                        department_id=row["department_id"],
                    )

        return None