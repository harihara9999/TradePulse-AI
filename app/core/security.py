from fastapi import Security, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from app.core.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_client_ip(request: Request) -> str:
    """Helper method to get client IP for rate limiting."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host if request.client else "127.0.0.1"

# Create a global rate limiter
limiter = Limiter(key_func=get_client_ip)

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """Validate the API Key provided in headers."""
    # We allow a guest mode or specific API key.
    if not api_key_header:
        # Fallback to guest mode
        return "guest"
        
    if api_key_header == settings.API_KEY:
        return api_key_header
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key provided",
    )
