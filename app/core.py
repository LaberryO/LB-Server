from fastapi import FastAPI, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

class Core:
    def __init__(self):
        self.app = FastAPI()
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory="/templates")

        self.app.mount("/static", StaticFiles(directory="static"), name="static")

    def setup_route(self):
        @self.router.get("/")
        def root(request: Request):
            client_ip = request.client.host
            ip_parts = client_ip.split(".")

            if len(ip_parts) == 4:
                last_octet = int(ip_parts[-1])
            else:
                last_octet = 0

            if last_octet > 0 and last_octet == 250:
                current_user = "ADMIN"
            else:
                current_user = "GUEST"

            self.templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "title": "SEOUL-DEV-MAIN-01",
                    "user": current_user
                }
            )

    def run(self):
        self.setup_route()
        self.app.include_router(self.router)

        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=80)