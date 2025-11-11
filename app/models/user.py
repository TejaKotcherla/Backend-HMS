from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    hashed_password = Column(String, nullable=False)

    gender = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)

    # Role management
    role = Column(String(50), nullable=False, default="patient")  
    # allowed: patient / doctor / admin

    department = Column(String(255), nullable=True)
    qualification = Column(String(255), nullable=True)
    experience = Column(String(50), nullable=True)
    blood_group = Column(String(10), nullable=True)

    # Account approval and active status
    status = Column(String(50), nullable=False, default="approved")  
    # pending | approved | rejected

    is_active = Column(Boolean, nullable=False, default=True)

    # ✅ Marks if the user is a system-created admin (cannot be deleted)
    is_system = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
