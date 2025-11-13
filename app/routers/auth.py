from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, crud
from ..deps import create_access_token, get_current_user
from ..database import get_db
from ..core.config import settings
from ..utils import verify_password
from ..models import User  # Correct model import

router = APIRouter(prefix="/api/auth", tags=["auth"])


# -------------------- USER / DOCTOR REGISTRATION --------------------
@router.post("/register", response_model=schemas.UserOut)
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    
    # Check if email already exists
    existing = await crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    new_user = await crud.create_user(db=db, user=user_in)

    # If doctor → mark as pending & notify admin
    if user_in.role.lower() == "doctor":
        new_user.status = "pending"
        await db.commit()
        await db.refresh(new_user)
        await crud.create_admin_request(db, new_user.id, "doctor_registration")

    return new_user



# -------------------- LOGIN / TOKEN GENERATION --------------------
@router.post("/token", response_model=schemas.TokenWithUser)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    username = form_data.username
    password = form_data.password

    # -------- SUPER ADMIN (ADMIN 1) --------
    if username == settings.admin1_email and password == settings.admin1_password:
        token = create_access_token(subject="admin1")

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "super_admin",
            "user": {
                "id": None,
                "first_name": "Super",
                "last_name": "Admin",
                "email": settings.admin1_email,
                "phone_number": None,
                "gender": None,
                "age": None,
                "city": None,
                "country": None,
                "role": "super_admin",
                "blood_group": None,
                "department": None,
                "qualification": None,
                "experience": None,
            }
        }

    # -------- ADMIN 2 --------
    if username == settings.admin2_email and password == settings.admin2_password:
        token = create_access_token(subject="admin2")

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "admin",
            "user": {
                "id": None,
                "first_name": "Admin",
                "last_name": "",
                "email": settings.admin2_email,
                "phone_number": None,
                "gender": None,
                "age": None,
                "city": None,
                "country": None,
                "role": "admin",
                "blood_group": None,
                "department": None,
                "qualification": None,
                "experience": None,
            }
        }

    # -------- NORMAL USER LOGIN --------
    result = await crud.authenticate_user(db, username, password)

    if result is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if result == "not_approved":
        raise HTTPException(status_code=403, detail="Doctor account pending approval")

    # Generate token
    token = create_access_token(subject=str(result.id))

    # User details returned to frontend
    user_out = {
        "id": result.id,
        "first_name": result.first_name,
        "last_name": result.last_name,
        "email": result.email,
        "phone_number": result.phone_number,
        "gender": result.gender,
        "age": result.age,
        "city": result.city,
        "country": result.country,
        "role": result.role,
        "blood_group": result.blood_group,
        "department": result.department,
        "qualification": result.qualification,
        "experience": result.experience,
    }

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": result.role,
        "user": user_out
    }



# -------------------- SELF PROFILE --------------------
@router.get("/me", response_model=schemas.UserOut)
async def get_logged_in_user(current_user: User = Depends(get_current_user)):
    return current_user
