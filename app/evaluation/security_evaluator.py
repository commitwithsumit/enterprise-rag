from pathlib import Path

from app.auth.clearance import has_clearance
from app.auth.permissions import has_permission
from app.auth.policy import role_can_access_resource
from app.models.user import User
from app.models.role import Role
from app.models.resource import Resource


class SecurityEvaluator:

    def __init__(self):
        self.base_path = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "rbac"
        )

        self.users = self._load_users()
        self.roles = self._load_roles()
        self.user_roles = self._load_user_roles()
        self.role_permissions = self._load_role_permissions()
        self.resources = self._load_resources()
        self.resource_roles = self._load_resource_roles()

    # --------------------------------------------------
    # LOAD USERS
    # --------------------------------------------------

    def _load_users(self):

        import csv

        path = self.base_path / "users.csv"
        users = {}

        with path.open(
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                users[row["username"]] = User(
                    user_id=row["user_id"],
                    username=row["username"],
                    full_name=row["full_name"],
                    email=row["email"],
                    department_id=row["department_id"],
                    status=row["status"],
                    clearance_level=row["clearance_level"],
                )

        return users

    # --------------------------------------------------
    # LOAD ROLES
    # --------------------------------------------------

    def _load_roles(self):

        import csv

        path = self.base_path / "roles.csv"
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

    # --------------------------------------------------
    # USER → ROLES
    # --------------------------------------------------

    def _load_user_roles(self):

        import csv

        path = self.base_path / "user_roles.csv"
        mapping = {}

        with path.open(
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                mapping.setdefault(
                    row["user_id"],
                    []
                ).append(row["role_id"])

        return mapping

    # --------------------------------------------------
    # ROLE → PERMISSIONS
    # --------------------------------------------------

    def _load_role_permissions(self):

        import csv

        path = self.base_path / "role_permissions.csv"
        mapping = {}

        with path.open(
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                mapping.setdefault(
                    row["role_id"],
                    set()
                ).add(row["permission_id"])

        # Convert permission IDs to permission codes
        permission_path = (
            self.base_path / "permissions.csv"
        )

        permission_codes = {}

        with permission_path.open(
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                permission_codes[
                    row["permission_id"]
                ] = row["permission_code"]

        result = {}

        for role_id, permission_ids in mapping.items():

            result[role_id] = {
                permission_codes[permission_id]
                for permission_id in permission_ids
                if permission_id in permission_codes
            }

        return result

    # --------------------------------------------------
    # RESOURCES
    # --------------------------------------------------

    def _load_resources(self):

        import csv

        path = self.base_path / "resources.csv"
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

    # --------------------------------------------------
    # RESOURCE → ROLES
    # --------------------------------------------------

    def _load_resource_roles(self):

        import csv

        path = (
            self.base_path
            / "resource_role_access.csv"
        )

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

    # --------------------------------------------------
    # GET USER CONTEXT
    # --------------------------------------------------

    def get_user_context(self, username: str):

        user = self.users[username]

        role_ids = self.user_roles.get(
            user.user_id,
            []
        )

        roles = [
            self.roles[role_id]
            for role_id in role_ids
            if role_id in self.roles
        ]

        permissions = set()

        for role_id in role_ids:

            permissions.update(
                self.role_permissions.get(
                    role_id,
                    set()
                )
            )

        return user, roles, permissions

    # --------------------------------------------------
    # CHECK RESOURCE ACCESS
    # --------------------------------------------------

    def can_access(
        self,
        username: str,
        resource_id: str,
        required_permission: str,
    ) -> bool:

        user, roles, permissions = (
            self.get_user_context(username)
        )

        resource = self.resources.get(
            resource_id
        )

        if resource is None:
            return False

        if user.status != "ACTIVE":
            return False

        if not has_permission(
            permissions,
            required_permission
        ):
            return False

        if not has_clearance(
            user.clearance_level,
            resource.classification
        ):
            return False

        allowed_roles = self.resource_roles.get(
            resource_id,
            set()
        )

        if not role_can_access_resource(
            roles,
            allowed_roles
        ):
            return False

        return True