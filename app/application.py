from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

from app.database import Base, engine
from app.user.controller import router as user_router
from app.template import Templates

from .controller import router as app_router
from .settings import settings

class ServerApplication(FastAPI):
    def __init__(self, title="LB-Server", version="1.0.0", **kwargs):
        super().__init__(title=title, version=version, **kwargs)

        self._templates = Templates(directory="templates")

        self._init_database()
        self._init_static()
        self._init_routers()
        self._init_middleware()

    def _init_database(self):
        Base.metadata.create_all(bind=engine)

    def _init_static(self):
        self.mount("/static", StaticFiles(directory="static"), name="static")
        self.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules")

    def _init_routers(self):
        self.include_router(app_router)
        self.include_router(user_router)

    def _init_middleware(self):
        @self.middleware("http")
        async def ip_whitelist_for_docs(request: Request, call_next):
            if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
                client_ip = request.client.host
                # TODO: need Authencation by Account. Not IP.
                if settings.debug_mode == True and client_ip != settings.dev_ip and client_ip != "127.0.0.1":
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Forbidden: Not-allowed IP"}
                    )
            return await call_next(request)

    @property
    def templates(self) -> Templates:
        return self._templates