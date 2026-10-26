CLASSIFICATION_LEVELS = {
    "PUBLIC": 1,
    "INTERNAL": 2,
    "CONFIDENTIAL": 3,
    "RESTRICTED": 4,
}


def has_clearance(user_clearance: str, resource_classification: str) -> bool:
    user_level = CLASSIFICATION_LEVELS.get(user_clearance)
    resource_level = CLASSIFICATION_LEVELS.get(resource_classification)

    if user_level is None:
        raise ValueError(f"Unknown user clearance: {user_clearance}")

    if resource_level is None:
        raise ValueError(
            f"Unknown resource classification: {resource_classification}"
        )

    return user_level >= resource_level