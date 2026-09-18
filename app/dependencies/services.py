from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.user import UserService, UserRepository

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)