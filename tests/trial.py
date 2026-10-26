
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RBAC_DIR = PROJECT_ROOT / "data" / "rbac"

def read_csv(filename):
    path = RBAC_DIR / filename
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def main():
    resources = read_csv("resources.csv")
    roles = read_csv("roles.csv")
    policies = read_csv("resource_role_access.csv")

    resource_ids = {row["resource_id"] for row in resources}
    role_ids = {row["role_id"] for row in roles}

    errors = []

    # Duplicate resource IDs
    resource_id_list = [row["resource_id"] for row in resources]
    if len(resource_id_list) != len(resource_ids):
        errors.append("Duplicate resource IDs found.")

    # Duplicate role IDs
    role_id_list = [row["role_id"] for row in roles]
    if len(role_id_list) != len(role_ids):
        errors.append("Duplicate role IDs found.")

    # Validate policy references
    for row in policies:
        if row["resource_id"] not in resource_ids:
            errors.append(
                f"Policy {row['access_policy_id']} references "
                f"unknown resource {row['resource_id']}."
            )
        if row["role_id"] not in role_ids:
            errors.append(
                f"Policy {row['access_policy_id']} references "
                f"unknown role {row['role_id']}."
            )

    # Detect duplicate resource-role combinations
    combinations = [
        (row["resource_id"], row["role_id"])
        for row in policies
    ]
    if len(combinations) != len(set(combinations)):
        errors.append("Duplicate resource-role policy combinations found.")

    print("Resources:", len(resources))
    print("Roles:", len(roles))
    print("Access policies:", len(policies))

    if errors:
        print("\nFAIL — RBAC consistency issues:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("\nPASS — All resource and role references are valid.")
    print("PASS — No duplicate resource-role combinations.")

if __name__ == "__main__":
    main()
