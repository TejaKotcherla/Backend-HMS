from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(db: AsyncSession, email: str):
    q = await db.execute(select(models.User).where(models.User.email == email))
    return q.scalars().first()

async def create_user(db: AsyncSession, user_in: schemas.UserCreate):
    hashed = pwd_context.hash(user_in.password)
    status = "pending" if user_in.role == "doctor" else "approved"

    db_user = models.User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        phone_number=user_in.phone_number,
        hashed_password=hashed,
        gender=user_in.gender,
        age=user_in.age,
        city=user_in.city,
        country=user_in.country,
        role=user_in.role,
        department=user_in.department,
        qualification=user_in.qualification,
        experience=user_in.experience,
        blood_group=user_in.blood_group,
        status=status,
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None

    # Restrict doctor login until approved
    if user.role == "doctor" and user.status != "approved":
        return "not_approved"

    return user

async def update_doctor_status(db: AsyncSession, user_id: int, new_status: str):
    await db.execute(update(models.User).where(models.User.id == user_id, models.User.role == "doctor").values(status=new_status))
    await db.commit()
    return True
