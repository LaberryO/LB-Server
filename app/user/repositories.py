from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception:
            self.db.rollback()
            raise
        
    def find_by_id(self, id: int) -> Optional[User]:
        return self.db.get(User, id)

    def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()