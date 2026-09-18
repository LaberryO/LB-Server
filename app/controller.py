from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.template import Templates
from app.dependencies.templates import get_templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def read_root(
    request: Request,
    templates: Templates = Depends(get_templates)
):
    
    # TODO: fix context
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "TEST TITLE",
            "user": "TEST USER",
        }
    )