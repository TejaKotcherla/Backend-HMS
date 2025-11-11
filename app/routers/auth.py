from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud
from ..deps import create_access_token
from ..database import get_db
from ..core.config import settings
from ..utils import verify_password  # ensure you have this imported

router = APIRouter(prefix="/api/auth", tags=["auth"])

# -------------------- USER REGISTRATION --------------------
@router.post("/register", response_model=schemas.UserOut)
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await crud.create_user(db=db, user=user_in)
    return new_user


# -------------------- LOGIN / TOKEN GENERATION --------------------
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    username = form_data.username
    password = form_data.password

    # ---------- FIXED ADMIN 1 ----------
    if username == settings.admin1_email and password == settings.admin1_password:
        access_token = create_access_token(subject=settings.admin1_email)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "super_admin"
        }

    # ---------- FIXED ADMIN 2 ----------
    if username == settings.admin2_email and password == settings.admin2_password:
        access_token = create_access_token(subject=settings.admin2_email)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "admin"
        }

    # ---------- NORMAL USER AUTHENTICATION ----------
    result = await crud.authenticate_user(db, username, password)

    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    if result == "not_approved":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor account pending approval from admin")

    access_token = create_access_token(subject=result.email)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": "user"
    }
