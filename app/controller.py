from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

def get_templates(request: Request) -> Jinja2Templates:
    return request.app.templates

@router.get("/", response_class=HTMLResponse)
def read_root(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates)
):
    # TODO: fix context
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "TEST TITLE",
            "user": "TEST USER"
        }
    )