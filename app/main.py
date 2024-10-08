from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import BytesIO
import base64

from app.auth.otp_manager import OTPManager
from app.auth.qrcode_manager import QRCodeManager

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

otp_manager = OTPManager()
qr_manager = QRCodeManager()


@app.get("/", response_class=RedirectResponse)
async def redirect_to_otp_issuance():
    return RedirectResponse(url="/otp_issuance")


@app.get("/otp_issuance", response_class=HTMLResponse)
async def otp_issuance_page(request: Request):

    return templates.TemplateResponse("otp_issuance.html", {"request": request})


@app.post("/generate_otp", response_class=HTMLResponse)
async def generate_otp(request: Request):

    otp_manager.generate_secret()
    print(otp_manager.secret)
    qr_code_uri = otp_manager.generate_qr_code_uri()

    qr_code_img = qr_manager.generate_qrcode(qr_code_uri)
    buffer = BytesIO()
    qr_code_img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return templates.TemplateResponse(
        "otp_issuance.html",
        {
            "request": request,
            "qr_code_img": qr_code_base64,
        },
    )


@app.post("/verify_otp", response_class=HTMLResponse)
async def verify_otp(request: Request, otp: str = Form(...)):
    is_valid = otp_manager.verify_otp(otp)
    print(is_valid)

    if is_valid:
        message = "OTP 인증 성공!"
    else:
        message = "OTP 인증 실패. 올바른 OTP를 입력해주세요."

    qr_code_uri = otp_manager.generate_qr_code_uri()
    qr_code_img = qr_manager.generate_qrcode(qr_code_uri)
    buffer = BytesIO()
    qr_code_img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return templates.TemplateResponse(
        "otp_issuance.html",
        {
            "request": request,
            "qr_code_img": qr_code_base64,
            "message": message,
        },
    )
