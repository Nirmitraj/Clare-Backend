# app/main.py
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import date
from app.config import settings
from app.routers import chat as chat_router 
from app.routers import contact

BASE_DIR = Path(__file__).resolve().parent          # .../backend/app
PROJECT_DIR = BASE_DIR.parent                       # .../backend
STATIC_DIR = PROJECT_DIR / "static"                 # put static here
TEMPLATES_DIR = BASE_DIR / "templates"              # app/templates

app = FastAPI(title="Clare Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use absolute paths
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.include_router(chat_router.router)
app.include_router(contact.router, prefix="/api") 
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "page.html",
        {"request": request, "title": "Clare Senior Care", "description": "Compassionate AFC/GAFC & home care."},
    )
