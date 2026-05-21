from pydantic import BaseModel


# Schema for user registration requests
class UserRegister(BaseModel):

    # User email for authentication
    email: str

    # Plain password received from client
    password: str


# Schema for user login requests
class UserLogin(BaseModel):

    # Registered user email
    email: str

    # User password for verification
    password: str