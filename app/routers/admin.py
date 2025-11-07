from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .. import schemas, models, crud
from ..database import get_db

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/pending-doctors", response_model=list[schemas.UserOut])
async def list_pending_doctors(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(models.User).where(models.User.role == "doctor", models.User.status == "pending"))
    return q.scalars().all()

@router.get("/notifications")
async def get_admin_notifications(db: AsyncSession = Depends(get_db)):
    pending_count_query = await db.execute(
        select(func.count(models.User.id)).where(models.User.role == "doctor", models.User.status == "pending")
    )
    pending_count = pending_count_query.scalar() or 0

    pending_list_query = await db.execute(
        select(models.User.id, models.User.first_name, models.User.last_name, models.User.department)
        .where(models.User.role == "doctor", models.User.status == "pending")
    )
    pending_doctors = [
        {
            "id": row.id,
            "name": f"{row.first_name} {row.last_name}",
            "department": row.department or "N/A",
        }
        for row in pending_list_query.fetchall()
    ]

    return {
        "pending_count": pending_count,
        "pending_doctors": pending_doctors,
    }

@router.put("/approve/{user_id}")
async def approve_doctor(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.update_doctor_status(db, user_id, "approved")
    if not success:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor approved successfully"}

@router.put("/reject/{user_id}")
async def reject_doctor(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.update_doctor_status(db, user_id, "rejected")
    if not success:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor rejected successfully"}
