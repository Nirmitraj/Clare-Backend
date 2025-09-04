# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import chat as chat_router
from app.routers import contact

app = FastAPI(title="Clare Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*settings.CORS_ORIGINS],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount ALL routers under /api
app.include_router(chat_router.router,    prefix="/api")   # -> /api/chat
app.include_router(contact.router,        prefix="/api")   # -> /api/contact

@app.get("/")
def health():
    return {"ok": True, "service": "clare-backend"}
