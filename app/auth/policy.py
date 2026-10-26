from app.models.role import Role


def role_can_access_resource(
    user_roles: list[Role],
    allowed_role_names: set[str],
) -> bool:

    user_role_names = {
        role.role_name
        for role in user_roles
    }

    return bool(
        user_role_names.intersection(allowed_role_names)
    )