from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy import ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    hashed_password = Column(String, nullable=False)
    gender = Column(String(10))
    age = Column(Integer)
    city = Column(String(100))
    country = Column(String(100))
    role = Column(String(50), nullable=False, default="patient")  # patient / doctor / admin
    department = Column(String(255), nullable=True)
    qualification = Column(String(255), nullable=True)
    experience = Column(String(50), nullable=True)
    blood_group = Column(String(10), nullable=True)
    status = Column(String(50), default="approved")  # pending | approved | rejected
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



class AdminRequest(Base):
    __tablename__ = "admin_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    request_type = Column(String(100), nullable=False)  # e.g., "doctor_registration"
    status = Column(String(50), default="pending")  # pending | approved | rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
