from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_user_service

from .services import UserService
from .models import UserCreateRequest, UserResponse

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/create")

@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(request: UserCreateRequest, service: UserService = Depends(get_user_service)) -> UserResponse:
    return service.create(request)

@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_by_id(id: int, service: UserService = Depends(get_user_service)) -> UserResponse:
    # TODO: need authentication
    return service.get_user_by_id(id)