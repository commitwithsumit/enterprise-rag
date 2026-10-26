from fastapi import Depends, FastAPI, HTTPException, status
from app.auth.dependencies import get_current_user
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.jwt_handler import create_access_token
from app.auth.password import verify_password
from app.repositories.credential_repository import CredentialRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token

from app.auth.authorization import authorize
from app.models.resource import Resource
from app.models.role import Role


app = FastAPI(
    title="Enterprise RAG Security API",
    version="0.1.0",
)


USER_FILE = "data/rbac/users.csv"
CREDENTIAL_FILE = "data/rbac/user_credentials.csv"


user_repository = UserRepository(USER_FILE)

credential_repository = CredentialRepository(
    CREDENTIAL_FILE
)


@app.get("/")
def root():

    return {
        "message": "Enterprise RAG Security API"
    }

@app.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):

    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "department_id": current_user.department_id,
        "clearance_level": current_user.clearance_level,
    }

@app.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    user = user_repository.get_by_username(
        form_data.username
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if user.status != "ACTIVE":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    password_hash = credential_repository.get_password_hash(
        form_data.username
    )

    if password_hash is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not verify_password(
        form_data.password,
        password_hash,
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(
        data={
            "sub": user.user_id,
            "username": user.username,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@app.get("/security-incidents")
def get_security_incidents(
    current_user: User = Depends(get_current_user),
):

    security_role = Role(
        role_id="R005",
        role_name="SECURITY_ANALYST",
        description="Security analyst",
    )

    security_resource = Resource(
        resource_id="RES006",
        resource_name="Security Incidents",
        resource_type="SQL_TABLE",
        classification="CONFIDENTIAL",
        department_id="D004",
    )

    permissions = {
        "READ_PUBLIC",
        "READ_INTERNAL",
        "READ_SECURITY",
        "READ_OPERATIONAL",
        "VIEW_SECURITY_EVENTS",
        "VIEW_RETRIEVAL_TRACE",
    }

    allowed = authorize(
        user=current_user,
        user_roles=[security_role],
        user_permissions=permissions,
        resource=security_resource,
        required_permission="READ_SECURITY",
        allowed_roles={
            "SECURITY_ANALYST",
            "SECURITY_ADMIN",
        },
    )

    if not allowed:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return {
        "message": "Security resource accessed successfully",
        "user": current_user.username,
        "resource": security_resource.resource_name,
    }