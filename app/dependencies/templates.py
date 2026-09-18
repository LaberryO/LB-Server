from fastapi import Request

from app.template import Templates

def get_templates(request: Request) -> Templates:
    return request.app.templates