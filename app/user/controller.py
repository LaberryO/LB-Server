from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import HTMLResponse

from app.dependencies.templates import get_templates
from app.dependencies.services import get_user_service
from app.template import Templates

from .services import UserService
from .models import UserCreateRequest, UserResponse

router = APIRouter(prefix="/user", tags=["Users"])

# MEMO: response_class == Content-Type
@router.get("/create", response_class=HTMLResponse)
def create_page(request: Request, templates: Templates = Depends(get_templates)) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="user/register.html"
    )

@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(request: UserCreateRequest, service: UserService = Depends(get_user_service)) -> UserResponse:
    return service.create(request)

# TODO: I think, this is not how to use it
# @router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
# def get_by_id(id: int, service: UserService = Depends(get_user_service)) -> UserResponse:
#     # TODO: need authentication
#     return service.get_user_by_id(id)

@router.get("/login", response_class=HTMLResponse)
def login(request: Request, templates: Templates = Depends(get_templates)) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="user/login.html"
    )