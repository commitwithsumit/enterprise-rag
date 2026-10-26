import csv
from pathlib import Path

from app.auth.clearance import has_clearance
from app.auth.permissions import has_permission
from app.auth.policy import role_can_access_resource

from app.models.resource import Resource
from app.models.role import Role
from app.models.user import User


BASE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "rbac"
)


class ResourceAccessService:

    def __init__(self):

        self.resources = self._load_resources()
        self.roles = self._load_roles()
        self.resource_roles = self._load_resource_roles()

    # -----------------------------------------
    # LOAD RESOURCES
    # -----------------------------------------

    def _load_resources(self):

        path = BASE_PATH / "resources.csv"

        resources = {}

        with path.open(
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                resources[row["resource_id"]] = Resource(
                    resource_id=row["resource_id"],
                    resource_name=row["resource_name"],
                    resource_type=row["resource_type"],
                    classification=row["classification"],
                    department_id=row["department_id"],
                )

        return resources

    # -----------------------------------------
    # LOAD ROLES
    # -----------------------------------------

    def _load_roles(self):

        path = BASE_PATH / "roles.csv"

        roles = {}

        with path.open(
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                roles[row["role_id"]] = Role(
                    role_id=row["role_id"],
                    role_name=row["role_name"],
                    description=row["description"],
                )

        return roles

    # -----------------------------------------
    # LOAD RESOURCE → ROLE MAPPING
    # -----------------------------------------

    def _load_resource_roles(self):

        path = BASE_PATH / "resource_role_access.csv"

        mapping = {}

        with path.open(
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                resource_id = row["resource_id"]
                role_id = row["role_id"]

                role = self.roles.get(role_id)

                if role is None:
                    continue

                mapping.setdefault(
                    resource_id,
                    set()
                ).add(role.role_name)

        return mapping

    # -----------------------------------------
    # AUTHORIZED RESOURCES
    # -----------------------------------------

    def get_authorized_resource_ids(
        self,
        user: User,
        user_roles: list[Role],
        user_permissions: set[str],
        required_permission: str,
    ) -> set[str]:

        if user.status != "ACTIVE":
            return set()

        authorized = set()

        for resource_id, resource in self.resources.items():

            allowed_roles = (
                self.resource_roles.get(
                    resource_id,
                    set()
                )
            )

            # Permission check
            if not has_permission(
                user_permissions,
                required_permission
            ):
                continue

            # Clearance check
            if not has_clearance(
                user.clearance_level,
                resource.classification
            ):
                continue

            # Role/resource check
            if not role_can_access_resource(
                user_roles,
                allowed_roles
            ):
                continue

            authorized.add(resource_id)

        return authorized