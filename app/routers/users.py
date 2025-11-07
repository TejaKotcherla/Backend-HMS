from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, crud
from ..deps import get_current_user
from ..database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", response_model=schemas.UserOut)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[schemas.UserOut])
async def list_users(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    q = await db.execute("SELECT * FROM users")
    rows = q.fetchall()
    users = []
    for r in rows:
        users.append({
            "id": r.id,
            "email": r.email,
            "first_name": r.first_name,
            "last_name": r.last_name,
            "phone_number": r.phone_number,
            "role": r.role,
            "is_active": r.is_active,
            "created_at": r.created_at,
        })
    return users
