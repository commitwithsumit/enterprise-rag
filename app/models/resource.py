from dataclasses import dataclass


@dataclass
class Resource:
    resource_id: str
    resource_name: str
    resource_type: str
    classification: str
    department_id: str