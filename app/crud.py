from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import verify_password, get_password_hash

# ==========================================================
# 🔹 Get user by email (used in register + login)
# ==========================================================
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

# ==========================================================
# 🔹 Create new user (used in register)
# ==========================================================
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        gender=user.gender,
        age=user.age,
        city=user.city,
        country=user.country,
        role=user.role,
        blood_group=user.blood_group,
        department=user.department,
        qualification=user.qualification,
        experience=user.experience,
        status="approved",  # Optional default
        is_active=True,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# ==========================================================
# 🔹 Authenticate user (used in login/token)
# ==========================================================
async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
