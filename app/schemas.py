from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

# ✅ Used for output in register/login
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # ✅ Pydantic v2 replacement for orm_mode

# ✅ Used for JWT Token response
class Token(BaseModel):
    access_token: str
    token_type: str

# ✅ Optional support schema
class TokenData(BaseModel):
    email: Optional[str] = None
