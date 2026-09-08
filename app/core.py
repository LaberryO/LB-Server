from fastapi import FastAPI, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

class Core:
    def __init__(self):
        self.app = FastAPI()
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory="templates")

        self.app.mount("/static", StaticFiles(directory="static"), name="static")

    def setup_route(self):
        @self.router.get("/")
        def root(request: Request):
            # 1. 프록시 환경이나 client가 없는 경우를 대비해 안전하게 IP 가져오기
            client_ip = None
            if request.client:
                client_ip = request.client.host
            
            # 만약 헤더에 실제 접속자 IP(예: X-Forwarded-For)가 있다면 그쪽을 우선 사용할 수도 있습니다.
            forwarded_for = request.headers.get("x-forwarded-for")
            if forwarded_for:
                client_ip = forwarded_for.split(",")[0].strip()

            if not client_ip:
                client_ip = "127.0.0.1" # 기본값 설정

            ip_parts = client_ip.split(".")

            if len(ip_parts) == 4:
                try:
                    last_octet = int(ip_parts[-1])
                except ValueError:
                    last_octet = 0
            else:
                last_octet = 0

            if last_octet > 0 and last_octet == 250:
                current_user = "ADMIN"
            else:
                current_user = "GUEST"

            return self.templates.TemplateResponse(
                request,
                "index.html",
                {
                    "title": "SEOUL-DEV-MAIN-01",
                    "user": current_user
                }
            )

    def run(self):
        self.setup_route()
        self.app.include_router(self.router)

        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=80)