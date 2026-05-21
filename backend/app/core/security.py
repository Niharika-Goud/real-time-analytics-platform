from datetime import datetime
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# JWT configuration
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"


# Password hashing configuration using bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Generate hashed password before storing in database
def hash_password(password: str):

    return pwd_context.hash(password)


# Verify plain password against hashed password
def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# Generate JWT access token with expiration
def create_access_token(data: dict):

    to_encode = data.copy()

    # Token expiration time
    expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )