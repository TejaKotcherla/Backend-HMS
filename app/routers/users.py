from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select

from app import schemas, models
from app.database import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


# -------------------------------------------
# 🔹 Get Logged-in User (Better version)
# -------------------------------------------
@router.get("/me", response_model=schemas.UserOut)
async def get_logged_in_user(
    current_user: models.User = Depends(get_current_user)
):
    return current_user


# -------------------------------------------
# 🔹 List all users (Admin only ideally)
# -------------------------------------------
@router.get("/", response_model=List[schemas.UserOut])
async def list_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # You can optionally restrict access:
    # if current_user.role not in ["admin", "super_admin"]:
    #     raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users
