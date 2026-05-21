from jose import jwt
from jose import JWTError

from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.database import get_db


# JWT configuration
from app.core.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"

# HTTP Bearer authentication scheme
security = HTTPBearer()


# Validate JWT token and fetch authenticated user
async def get_current_user(

    credentials: HTTPAuthorizationCredentials = Depends(security),

    db: AsyncSession = Depends(get_db)

):

    token = credentials.credentials

    # Common authentication error response
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token"
    )

    try:

        # Decode JWT token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        # Validate token payload
        if not email:

            raise credentials_exception

    except JWTError:

        raise credentials_exception

    # Fetch user from database
    result = await db.execute(

        select(User).where(
            User.email == email
        )

    )

    user = result.scalar_one_or_none()

    # Validate user existence
    if not user:

        raise credentials_exception

    return user


# Role-based access control helper
def require_roles(allowed_roles: list):

    async def role_checker(

        current_user: User = Depends(
            get_current_user
        )

    ):

        # Check if user role is authorized
        if current_user.role not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return current_user

    return role_checker