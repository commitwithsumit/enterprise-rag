from app.auth.authorization import authorize
from app.models.user import User
from app.models.role import Role
from app.models.resource import Resource


def test_security_analyst_can_access_security_resource():

    user = User(
        user_id="U014",
        username="kavya.reddy",
        full_name="Kavya Reddy",
        email="kavya.reddy@technova.example",
        department_id="D004",
        status="ACTIVE",
        clearance_level="CONFIDENTIAL",
    )

    roles = [
        Role(
            role_id="R005",
            role_name="SECURITY_ANALYST",
            description="Security analyst",
        )
    ]

    permissions = {
        "READ_PUBLIC",
        "READ_INTERNAL",
        "READ_SECURITY",
        "READ_OPERATIONAL",
        "VIEW_SECURITY_EVENTS",
        "VIEW_RETRIEVAL_TRACE",
    }

    resource = Resource(
        resource_id="RES006",
        resource_name="Security Incidents",
        resource_type="SQL_TABLE",
        classification="CONFIDENTIAL",
        department_id="D004",
    )

    result = authorize(
        user=user,
        user_roles=roles,
        user_permissions=permissions,
        resource=resource,
        required_permission="READ_SECURITY",
        allowed_roles={"SECURITY_ANALYST", "SECURITY_ADMIN"},
    )

    print(f"\nSecurity Analyst access: {result}")

    assert result is True


def test_employee_cannot_access_security_resource():

    user = User(
        user_id="U001",
        username="aarav.sharma",
        full_name="Aarav Sharma",
        email="aarav.sharma@technova.example",
        department_id="D001",
        status="ACTIVE",
        clearance_level="INTERNAL",
    )

    roles = [
        Role(
            role_id="R001",
            role_name="EMPLOYEE",
            description="Standard employee",
        )
    ]

    permissions = {
        "READ_PUBLIC",
        "READ_INTERNAL",
    }

    resource = Resource(
        resource_id="RES006",
        resource_name="Security Incidents",
        resource_type="SQL_TABLE",
        classification="CONFIDENTIAL",
        department_id="D004",
    )

    result = authorize(
        user=user,
        user_roles=roles,
        user_permissions=permissions,
        resource=resource,
        required_permission="READ_SECURITY",
        allowed_roles={"SECURITY_ANALYST", "SECURITY_ADMIN"},
    )

    print(f"Employee access to security resource: {result}")

    assert result is False


if __name__ == "__main__":
    test_security_analyst_can_access_security_resource()
    test_employee_cannot_access_security_resource()

    print("\nDay 1 RBAC tests completed successfully!")