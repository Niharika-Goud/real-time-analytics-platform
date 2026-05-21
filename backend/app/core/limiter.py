from slowapi import Limiter
from slowapi.util import get_remote_address


# Rate limiter configuration based on client IP address
limiter = Limiter(
    key_func=get_remote_address
)