def has_permission(
    user_permissions: set[str],
    required_permission: str,
) -> bool:
    return required_permission in user_permissions