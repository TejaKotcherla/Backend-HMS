from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ==========================================================
# 🔹 Base User Schema
# ==========================================================
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    gender: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    city: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    role: str  # "patient" | "doctor" | "admin"
    blood_group: Optional[str] = Field(default=None)
    department: Optional[str] = Field(default=None)
    qualification: Optional[str] = Field(default=None)
    experience: Optional[str] = Field(default=None)

# ==========================================================
# 🔹 User Create Schema (for /register)
# ==========================================================
class UserCreate(UserBase):
    password: str

# ==========================================================
# 🔹 Output Schema (for responses)
# ==========================================================
class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    gender: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    role: str
    blood_group: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None

    class Config:
        orm_mode = True  # ✅ replaces orm_mode in Pydantic v2

# ==========================================================
# 🔹 JWT Token Models
# ==========================================================
class Token(BaseModel):
    access_token: str
    token_type: str

# ==========================================================
# 🔹 Token with User (for login response)
# ==========================================================
class TokenWithUser(BaseModel):
    access_token: str
    token_type: str
    role: str
    user: Optional[UserOut] = None


class TokenData(BaseModel):
    email: Optional[str] = None
