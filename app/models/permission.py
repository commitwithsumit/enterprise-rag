from dataclasses import dataclass


@dataclass
class Permission:
    permission_id: str
    permission_code: str
    resource_type: str
    description: str