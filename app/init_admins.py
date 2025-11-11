from app import crud, schemas
from app.database import async_session_maker
from app.core.config import settings


async def init_admins():
    """Initialize default system admin accounts."""
    async with async_session_maker() as db:
        # Check if Admin 1 already exists
        admin1 = await crud.get_user_by_email(db, settings.admin1_email)
        if not admin1:
            admin_data = schemas.UserCreate(
                first_name="System",
                last_name="Admin1",
                email=settings.admin1_email,
                phone_number="9999999999",
                password=settings.admin1_password,  # plain text (hashed inside crud)
                role="admin",
                is_system=True
            )
            await crud.create_user(db=db, user=admin_data)
            print(f"✅ Created system admin: {settings.admin1_email}")

        # Check if Admin 2 already exists
        admin2 = await crud.get_user_by_email(db, settings.admin2_email)
        if not admin2:
            admin_data = schemas.UserCreate(
                first_name="System",
                last_name="Admin2",
                email=settings.admin2_email,
                phone_number="8888888888",
                password=settings.admin2_password,  # plain text (hashed inside crud)
                role="admin",
                is_system=True
            )
            await crud.create_user(db=db, user=admin_data)
            print(f"✅ Created system admin: {settings.admin2_email}")

        print("✅ Admin initialization complete")
