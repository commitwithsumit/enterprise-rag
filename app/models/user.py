from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    username: str
    full_name: str
    email: str
    department_id: str
    status: str
    clearance_level: str