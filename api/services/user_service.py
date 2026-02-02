from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from services.auth_service import AuthService


class UserService:

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=AuthService.get_password_hash(user_data.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
