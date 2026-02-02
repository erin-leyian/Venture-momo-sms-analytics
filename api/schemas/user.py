from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """User registration"""
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    """User login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response"""
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True
