from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from .repositories import UserRepository
from .services import UserService
from .models import UserCreateRequest, UserResponse

router = APIRouter(prefix="/user", tags=["Users"])

# TODO: NOT IMPORTANT - refactor this code after make dependencies.py
def get_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)

@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(request: UserCreateRequest, service: UserService = Depends(get_service)) -> UserResponse:
    return service.create(request)

@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_by_id(id: int, service: UserService = Depends(get_service)) -> UserResponse:
    # TODO: need authentication
    return service.get_user_by_id(id)