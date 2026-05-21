from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.security import create_access_token

from app.models.user import User

from app.schemas.user import UserRegister
from app.schemas.user import UserLogin


# Authentication router for user registration and login
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Register a new user account
@router.post("/register")
async def register_user(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db)
):

    # Check if email already exists
    query = select(User).where(
        User.email == payload.email
    )

    result = await db.execute(query)

    existing_user = result.scalar_one_or_none()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Create new user with hashed password
    user = User(
        email=payload.email,
        password_hash=hash_password(
            payload.password
        )
    )

    db.add(user)

    await db.commit()

    return {
        "message": "User registered successfully"
    }


# Login endpoint for JWT token generation
@router.post("/login")
async def login_user(
    payload: UserLogin,
    db: AsyncSession = Depends(get_db)
):

    # Fetch user using email
    query = select(User).where(
        User.email == payload.email
    )

    result = await db.execute(query)

    user = result.scalar_one_or_none()

    # Validate user existence
    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Verify hashed password
    valid_password = verify_password(
        payload.password,
        user.password_hash
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Generate JWT access token
    token = create_access_token({
        "sub": user.email
    })

    return {
        "access_token": token
    }