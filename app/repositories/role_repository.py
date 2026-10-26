import csv
from pathlib import Path

from app.models.role import Role


class RoleRepository:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get_by_id(self, role_id: str) -> Role | None:

        with self.file_path.open(
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["role_id"] == role_id:
                    return Role(
                        role_id=row["role_id"],
                        role_name=row["role_name"],
                        description=row["description"],
                    )

        return None