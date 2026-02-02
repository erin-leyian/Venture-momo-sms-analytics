from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Schema for access token response"""
    access_token: str
    token_type: str = "bearer"


class TokenPair(BaseModel):
    """Schema for access and refresh token pair"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str
