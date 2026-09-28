import hashlib, base64, string, secrets, requests

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.settings import settings
from app.template import Templates
from app.dependencies.templates import get_templates

router = APIRouter(prefix="/rcs")

def sha512_to_base64(text: str) -> str:
    sha = hashlib.sha512(text.encode("utf-8")).digest()
    return base64.b64encode(sha).decode("utf-8")

@router.get("/", response_class=HTMLResponse)
def rcs_console(
    request: Request,
    templates: Templates = Depends(get_templates)
):
    chars = string.ascii_letters + string.digits + "-_"
    random_str = "".join(secrets.choice(chars) for _ in range(16))

    step1 = sha512_to_base64(settings.api_password)
    encrypted_password = sha512_to_base64(f"{step1}.{random_str}")

    url = f"{settings.api_url}/auth/v1/{random_str}"
    payload = {
        "apiKey": settings.api_key,
        "apiPwd": encrypted_password
    }

    response = requests.post(url, json=payload)
    res_data = response.json()

    if res_data.get("code") == "10000":
        access_token = res_data["data"]["token"]
        refresh_token = res_data["data"]["refreshToken"]
        print("발급 성공!")
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)
    else:
        print("발급 실패:", res_data)

    return templates.TemplateResponse(
        request=request,
        name="rcs/web_console.html",
        context={
            "token": access_token
        }
    )