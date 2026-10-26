from app.auth.clearance import has_clearance
from app.auth.permissions import has_permission
from app.auth.policy import role_can_access_resource
from app.models.resource import Resource
from app.models.role import Role
from app.models.user import User


def authorize(
    user: User,
    user_roles: list[Role],
    user_permissions: set[str],
    resource: Resource,
    required_permission: str,
    allowed_roles: set[str],
) -> bool:

    # 1. User must be active
    if user.status != "ACTIVE":
        return False

    # 2. Check required permission
    if not has_permission(
        user_permissions,
        required_permission,
    ):
        return False

    # 3. Check clearance level
    if not has_clearance(
        user.clearance_level,
        resource.classification,
    ):
        return False

    # 4. Check resource-level role policy
    if not role_can_access_resource(
        user_roles,
        allowed_roles,
    ):
        return False

    return True