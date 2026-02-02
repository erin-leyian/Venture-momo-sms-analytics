from fastapi import APIRouter, Depends
from models.user import User
from schemas.user import UserResponse
from dependencies.auth import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user
