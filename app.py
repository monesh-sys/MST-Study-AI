from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from PIL import Image
import pytesseract
import io
import fitz

from pydantic import BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from ai import get_ai_reply

from dotenv import load_dotenv
import os
import asyncio

# ---------------- LOAD ENV ----------------
load_dotenv()

app = FastAPI()

# ---------------- STATIC FILES ----------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- OCR CONFIG ----------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------- EMAIL CONFIG ----------------
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

# ---------------- REVIEW MODEL ----------------
class Review(BaseModel):
    email: str
    message: str


# ---------------- HOME ----------------
@app.get("/")
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# ---------------- CHAT ----------------
@app.post("/chat")
async def chat(data: dict):
    try:
        reply = await asyncio.to_thread(get_ai_reply, data["message"])
        return JSONResponse({"reply": reply})
    except Exception:
        return JSONResponse(
            {"reply": "Error processing chat request"},
            status_code=500
        )


# ---------------- IMAGE UPLOAD (OCR) ----------------
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...), task: str = Form("")):

    if file.content_type not in ["image/png", "image/jpeg"]:
        return JSONResponse({"reply": "Only PNG/JPG allowed"}, status_code=400)

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("L")

        text = pytesseract.image_to_string(image, config="--psm 6")

        prompt = f"""
You are an exam assistant AI.

TASK: {task}

IMAGE TEXT:
{text}

Give a short, clear exam answer.
"""

        result = await asyncio.to_thread(get_ai_reply, prompt)

        return JSONResponse({"reply": result})

    except Exception:
        return JSONResponse({"reply": "Image processing failed"}, status_code=500)


# ---------------- PDF UPLOAD ----------------
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), task: str = Form("")):

    if file.content_type != "application/pdf":
        return JSONResponse({"reply": "Only PDF allowed"}, status_code=400)

    try:
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = "\n".join(page.get_text("text") for page in doc)

        prompt = f"""
You are an exam assistant AI.

TASK: {task}

PDF CONTENT:
{text}

Give short, well-structured notes.
"""

        result = await asyncio.to_thread(get_ai_reply, prompt)

        return JSONResponse({"reply": result})

    except Exception:
        return JSONResponse({"reply": "PDF processing failed"}, status_code=500)


# ---------------- SEND REVIEW EMAIL ----------------
@app.post("/send-review")
async def send_review(data: Review):

    try:
        html = f"""
        <h2>📩 MST Study AI Review</h2>
        <p><b>Email:</b> {data.email}</p>
        <p><b>Message:</b> {data.message}</p>
        """

        message = MessageSchema(
            subject="New Review - MST Study AI",
            recipients=[os.getenv("MAIL_USERNAME")],
            body=html,
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)

        return {"status": "success", "message": "Email sent successfully"}

    except Exception:
        return {"status": "error", "message": "Email failed"}


# ---------------- PRIVACY POLICY ----------------
@app.get("/privacy-policy")
def privacy_policy():
    return FileResponse("privacy_policy.html")


# ---------------- TERMS ----------------
@app.get("/terms")
def terms():
    return FileResponse("terms.html")
