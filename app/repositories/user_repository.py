import csv
from pathlib import Path
from app.models.user import User


class UserRepository:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get_by_username(self, username: str) -> User | None:

        with self.file_path.open(
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["username"] == username:

                    return User(
                        user_id=row["user_id"],
                        username=row["username"],
                        full_name=row["full_name"],
                        email=row["email"],
                        department_id=row["department_id"],
                        status=row["status"],
                        clearance_level=row["clearance_level"],
                    )

        return None

    def get_by_id(self, user_id: str) -> User | None:

        with self.file_path.open(
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["user_id"] == user_id:

                    return User(
                        user_id=row["user_id"],
                        username=row["username"],
                        full_name=row["full_name"],
                        email=row["email"],
                        department_id=row["department_id"],
                        status=row["status"],
                        clearance_level=row["clearance_level"],
                    )

        return None