import csv
from pathlib import Path


class CredentialRepository:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get_password_hash(self, username: str) -> str | None:

        with self.file_path.open(
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["username"] == username:
                    return row["password_hash"]

        return None