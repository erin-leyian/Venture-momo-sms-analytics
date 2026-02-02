from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import get_db
from schemas.user import UserCreate, UserResponse, UserLogin
from schemas.token import TokenPair
from services.auth_service import AuthService
from services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    if UserService.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if UserService.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return UserService.create_user(db, user_data)


@router.post("/login", response_model=TokenPair)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login and get tokens"""
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return AuthService.create_token_pair(user)
    
    # Create new access token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "username": user.username
    }
    access_token = AuthService.create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}
