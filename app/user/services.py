from fastapi import HTTPException

from app.security import hash_password

from .repositories import UserRepository
from .models import User, UserCreateRequest, UserResponse

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create(self, request: UserCreateRequest) -> UserResponse:
        if self.repo.find_by_email(request.email):
            raise HTTPException(
                status_code=409,
                detail="Already registered email address."
            )

        new_entity = User(
            name = request.name,
            email = request.email,
            password = hash_password(request.password)
        )
        saved_entity = self.repo.save(new_entity)

        return UserResponse.model_validate(saved_entity)

    def get_user_by_id(self, id: int) -> UserResponse:
        response = self.repo.find_by_id(id)

        if not response:
            # TODO: Will Make Multiple Language
            raise HTTPException(status_code=404, detail="Not Found User")

        return UserResponse.model_validate(response)