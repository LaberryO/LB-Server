from pathlib import Path
from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates

class Templates(Jinja2Templates):
    def __init__(self, directory="templates", static_dir="static", **kwargs):
        super().__init__(directory=directory, **kwargs)
        self.static_dir = Path(static_dir)

    def TemplateResponse(
        self,
        request: Request,
        name: str,
        context: dict[str, Any] | None = None,
        **kwargs
    ):
        context = context or {}
        stem = Path(name).with_suffix("")

        # if css file exists, use its path. otherwise, use blank.css
        css_rel = f"css/{stem}.css"
        context["page_css"] = f"/static/{css_rel}" if (self.static_dir / css_rel).exists() else "/static/css/blank.css"

        # if js file exists, use its path. otherwise, use blank.js
        js_rel = f"js/{stem}.js"
        context["page_js"] = f"/static/{js_rel}" if (self.static_dir / js_rel).exists() else "/static/js/blank.js"

        return super().TemplateResponse(
            request=request,
            name=name,
            context=context,
            **kwargs
        )