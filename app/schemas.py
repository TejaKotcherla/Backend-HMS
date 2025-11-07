from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    gender: Optional[str]
    age: Optional[int]
    city: Optional[str]
    country: Optional[str]

class UserCreate(UserBase):
    password: str
    role: str  # patient | doctor
    department: Optional[str]
    qualification: Optional[str]
    experience: Optional[str]
    blood_group: Optional[str]

class UserOut(UserBase):
    id: int
    role: str
    department: Optional[str]
    qualification: Optional[str]
    experience: Optional[str]
    blood_group: Optional[str]
    status: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class StatusUpdate(BaseModel):
    status: str  # pending | approved | rejected

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None
