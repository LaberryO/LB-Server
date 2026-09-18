from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, ConfigDict

from app.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str

    model_config = ConfigDict(extra="ignore")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)