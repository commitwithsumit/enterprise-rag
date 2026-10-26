from dataclasses import dataclass


@dataclass
class Role:
    role_id: str
    role_name: str
    description: str