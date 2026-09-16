from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

from app.database import Base, engine
from app.user.controller import router as user_router

from .settings import settings

templates = Jinja2Templates(directory="templates")

class ServerApplication(FastAPI):
    def __init__(self, title="SJJEONG-DEV-SERVER", version="1.0.0", **kwargs):
        super().__init__(title=title, version=version, **kwargs)
        self.title = title

        self._init_database()
        self._init_routers()
        self._init_middleware()

    def _init_database(self):
        Base.metadata.create_all(bind=engine)

    def _init_routers(self):
        self.include_router(user_router)

        @self.get("/", response_class=HTMLResponse)
        def read_root(request: Request):
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "title": self.title,
                    "user": "TEST"
                }
            )

    def _init_middleware(self):
        @self.middleware("http")
        async def ip_whitelist_for_docs(request: Request, call_next):
            if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
                client_ip = request.client.host
                if client_ip != settings.dev_ip and client_ip != "127.0.0.1":
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Forbidden: Not-allowed IP"}
                    )
            return await call_next(request)