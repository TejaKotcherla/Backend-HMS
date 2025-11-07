from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud
from ..deps import create_access_token
from ..database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut)
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await crud.create_user(db, user_in)
    return new_user



@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await crud.authenticate_user(db, form_data.username, form_data.password)

    if result is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if result == "not_approved":
        raise HTTPException(status_code=403, detail="Doctor account pending approval from admin")

    access_token = create_access_token(subject=result.email)
    return {"access_token": access_token, "token_type": "bearer"}
