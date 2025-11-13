from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from .core.config import settings
from .database import get_db
from . import crud

# Token URL for OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Validate JWT token and return current user"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = await crud.get_user_by_id(db, int(user_id))

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


def create_access_token(subject: str, expires_delta: timedelta | None = None):
    """Generate JWT access token"""
    
    # Use provided expire time OR fallback to settings
    if expires_delta is None:
        # Try both naming styles (prevent crashing)
        expire_minutes = getattr(
            settings,
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            getattr(settings, "access_token_expire_minutes", 30)
        )
        expires_delta = timedelta(minutes=int(expire_minutes))

    expire = datetime.utcnow() + expires_delta

    to_encode = {
        "sub": str(subject),
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,       # Must be uppercase (your settings uses CAPS)
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt
